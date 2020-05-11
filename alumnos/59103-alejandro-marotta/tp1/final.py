import array
import re
from multiprocessing import Process , Queue
from argparse import ArgumentParser
import sys
import os.path


# funcion para obtener los argumentos
def parseArguments():

    analizador = ArgumentParser(description='Dividir imagen ppm en rojo,verde y azul')

    analizador.add_argument("-r","--red",type=int,default=1,help = "Escala de rojo")
    analizador.add_argument("-g","--green",type=int,default=1,help = "Escala de verde")
    analizador.add_argument("-b","--blue",type=int,default=1,help = "Escala de azul")
    analizador.add_argument("-f","--file",required=True,help = "Imagen ppm a analizar") #si o si hay que ingresarlo
    analizador.add_argument("-s","--size",type=int,default=1024,help = "Bloque de lectura")      

    return analizador.parse_args()


#funciones para cada uno de los hijos

def red(q_red,encabezado,r,nombre):
    
    rojo = []
    cuerpo = b''
#si pongo que analice pedacito por pedsacito, cuando el size no era multiplo de 3 se torcia
    while True:
        #se queda esperando a que hayan mensajes, no me parece necesario usar el if not queue.empty()
        mensaje = q_red.get()

        if mensaje == "finish":
            break
        else:
            cuerpo = cuerpo + mensaje

    #al iterar python convierte los valores en decimales
    pixels = [i for i in cuerpo]            

    for j in range(0,len(pixels),3):
        valor = pixels[j]*r
        if valor > 255:
            valor = 255
        rojo.append(valor)
        rojo.append(0)
        rojo.append(0)

#rearmo el archivo ppm
#https://solarianprogrammer.com/2017/10/25/ppm-image-python-3/
    rojo = array.array('B',rojo)

    with open('{}_red.ppm'.format(nombre), 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        rojo.tofile(f)


def green(q_green,encabezado,g,nombre):
    
    green = []
    cuerpo = b''

    while True:
        
        mensaje = q_green.get()

        if mensaje == "finish":
            break
        else:
            cuerpo = cuerpo + mensaje

    
    pixels = [i for i in cuerpo]            

    for j in range(1,len(pixels),3):
        valor = pixels[j]*g
        if valor > 255:
            valor = 255
        green.append(0)
        green.append(valor)
        green.append(0)

    green = array.array('B',green)

    with open('{}_green.ppm'.format(nombre), 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        green.tofile(f)


def blue(q_blue,encabezado,b,nombre):
    
    blue = []
    cuerpo = b''
#si pongo que analice pedacito por pedacito, cuando el size no era multiplo de 3 se torcia
    while True:
        #se queda esperando a que hayan mensajes, no me parece necesario usar el if not queue.empty()
        mensaje = q_blue.get()

        if mensaje == "finish":
            break
        else:
            cuerpo = cuerpo + mensaje

    #al iterar python convierte los valores en decimales
    pixels = [i for i in cuerpo]            

    for j in range(2,len(pixels),3):
        valor = pixels[j]*b
        if valor > 255:
            valor = 255
        blue.append(0)
        blue.append(0)
        blue.append(valor)

    blue = array.array('B',blue)

    with open('{}_blue.ppm'.format(nombre), 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        blue.tofile(f)
       


if __name__ == "__main__":

    #Traigo los argumentos  
    arg = parseArguments()

    r = arg.red
    g = arg.green
    b = arg.blue
    s = arg.size
    f = arg.file

    #si algun valor es negativo
    try:
        if (r<0) or (g<0) or (b<0) or (s<0):
            raise ValueError

    except ValueError:
        print("Los valores deben ser positivos")
        print("Intentelo de nuevo")
        sys.exit()
   


    #abro el archivo, rb lo lee como bytes https://docs.python.org/3/library/functions.html#open
    #me lo lee con hexa y ascii
    
    try:
        fd = open(f, "rb")  #si no existe larga un FileNotFoundError
        nombre, extension = os.path.splitext(f) #divido el nombre de la extension
        
        if extension != ".ppm": #compruebo que sea un archivo ppm
            raise UserWarning

    except FileNotFoundError:
        print("El archivo no existe")
        print("Intentelo de nuevo")
        sys.exit()
    
    except UserWarning:
        print("El archivo no es de tipo ppm")
        print("Intentelo de nuevo")
        sys.exit()

    

    #leo el principio del archivo para buscar el encabezado
    leido = fd.read(150)

    #utilizo re.finditer, el cual busca todas las posiciones donde se encuentra \n, a diferencia de find()
    #https://es.stackoverflow.com/questions/272517/c%C3%B3mo-buscar-un-caracter-en-string-python
    #la ultima posicion que encuentra se la otorgo a la variable valor
    for c in re.finditer(b'\n', leido):
    
        valor = c.end()

    #separo el encabezado y el cuerpo del pedacito que lei
    #TypeError: encoding or errors without a string argument si no pongo decode()
    encabezado = leido[:valor].decode()

    #el resto de la primera parte leida la guardo como cuerpo y se los envio a los hijos
    cuerpo = leido[valor:]

#creo las 3 colas
    q_red = Queue()
    q_green = Queue()
    q_blue = Queue()

#creo los 3 hijos
    h_red = Process(target=red, args= (q_red,encabezado,r,nombre))
    h_green = Process(target=green, args= (q_green,encabezado,g,nombre))
    h_blue = Process(target=blue, args= (q_blue,encabezado,b,nombre))

#arranco los 3 hijos
    h_red.start()
    h_green.start()
    h_blue.start()

#envio la primera parte del cuerpo
    q_red.put(cuerpo)
    q_green.put(cuerpo)
    q_blue.put(cuerpo)

#leo de a parte el archivo y se los envio a los hijos a la cola de mensajes
# hasta que lo que leo es mas chico que el size dado
    while True:
        cuerpo = fd.read(s)
        q_red.put(cuerpo)
        q_green.put(cuerpo)
        q_blue.put(cuerpo)
    
        if len(cuerpo) != s:
            break
    

#envio mensajes de finalizacion, como son colas FIFO siempre iran al final 
    q_red.put("finish")
    q_green.put("finish")
    q_blue.put("finish")

#el padre espera a que los hijos terminen   
    h_red.join()
    h_green.join()
    h_blue.join()

    #if los archivos red , blue y green.ppm estan en el directorio, archivos creados con exito
    #os.path.exists() devuelve true si existe o false si no

    if os.path.exists('{}_red.ppm'.format(nombre)) and os.path.exists('{}_green.ppm'.format(nombre)) and os.path.exists('{}_blue.ppm'.format(nombre)):
        print ("Archivos creados con exito")
    else:
        print("Uno o mas archivos no fueron creados")

#Cierro el archivo
    fd.close()

    



