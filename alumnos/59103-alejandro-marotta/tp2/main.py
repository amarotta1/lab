from esteganografia import esteganografo
from Hilo_return import Hilo
from escritor import escribir
from lector import leer
from control import control

from argparse import ArgumentParser
import array
import re
import sys
import os.path
from time import time


# funcion para obtener los argumentos
def parseArguments():

    analizador = ArgumentParser(description='Esteganografía')

    analizador.add_argument("-e","--offset",type=int,default=1,help = "Primer pixel donde se aplica el metodo de esteganografía")
    analizador.add_argument("-i","--interleave",type=int,default=1,help = "Cada cuantos pixels se aplica")
    analizador.add_argument("-f","--file",required=True,help = "Imagen ppm a analizar")
    analizador.add_argument("-m","--message",required=True,help = "Archivo con mensaje a encriptar")
    analizador.add_argument("-o","--output",required=True,help = "Nombre archivo de salida")
    analizador.add_argument("-s","--size",type=int,default=1026,help = "Bloque de lectura, debe ser multiplo de 3")      

    return analizador.parse_args()


  

if __name__ == "__main__":

    arg = parseArguments()

    offset = arg.offset
    interleave = arg.interleave
    f = arg.file
    message = arg.message
    output = arg.output +".ppm"
    size = arg.size

    time_i = time()

    try:
        if (offset<=0) or (interleave<=0) or (size<=0):
            raise ValueError

    except ValueError:
        print("Los valores deben ser positivos")
        print("Intentelo de nuevo")
        sys.exit()

    
    if size%3 != 0:
        print("ERROR, El size debe ser multiplo de 3")
        sys.exit()


##################################################################
   
    #Leo el archivo que contiene el mensaje
    hilo_lector = Hilo(target=leer,args=(message,))

    hilo_lector.start()
       
###################################################################

    #abro el archivo, rb lo lee como bytes 
    #me lo lee con hexa y ascii
    
    try:
        fd_image = open(f, "rb")  #si no existe larga un FileNotFoundError
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
    leido_imagen = fd_image.read(150)

    #utilizo re.finditer, el cual busca todas las posiciones donde se encuentra \n, a diferencia de find()
    #la ultima posicion que encuentra se la otorgo a la variable valor
    for c in re.finditer(b'\n', leido_imagen):
    
        valor = c.end()

    #separo el encabezado del pedacito que lei
    #TypeError: encoding or errors without a string argument si no pongo decode()
    encabezado = leido_imagen[:valor].decode()
      
    fd_image.seek(valor) #vuelvo hasta donde comienza el cuerpo 

    inicio = (offset-1)*3 #leo hasta el pixel anterior del offset donde quiero empezar

    cuerpo = fd_image.read(inicio)

    pixels = [i for i in cuerpo]  

    pixels = array.array('B',pixels) 

    #para que el hilo main siga haciendo sus cosas hasta que necesito los valores
    mensaje_str , longitud = hilo_lector.join()


    #una vez que tengo el encabezado y el largo del mensaje controlo que no sea mas grande

    control(encabezado,interleave,longitud,offset)

    #agrego el comentario de la UM

    comentario = "#UMCOMPU2 {} {} {}\n".format(offset,interleave,longitud)

    #Como tiene que arrancar siempre con PX 
    encabezado = encabezado[0:2] +"\n"+ comentario + encabezado[2:]

    #Guardo hasta ahi en el nuevo archivo
    with open(output, 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        pixels.tofile(f)
 
    

    #Comienza en el cuerpo
    comienzo_rojo = 0
    comienzo_verde = 1+ interleave *3
    comienzo_azul = 2+ 2*interleave *3


    #Comienza en el mensaje
    indice_rojo = 0
    indice_verde = 1
    indice_azul = 2


    # hasta que los 3 indices superen el valor de la longitud del mensaje == todo encriptado
    while True:
        cuerpo = fd_image.read(size)

        pixels1 = [i for i in cuerpo]
        pixels2 = [i for i in cuerpo]
        pixels3 = [i for i in cuerpo]

              
        hilo_rojo = Hilo(target=esteganografo,args=(mensaje_str,pixels1,indice_rojo,comienzo_rojo,interleave))
        hilo_verde = Hilo(target=esteganografo,args=(mensaje_str,pixels2,indice_verde,comienzo_verde,interleave))
        hilo_azul =  Hilo(target=esteganografo,args=(mensaje_str,pixels3,indice_azul,comienzo_azul,interleave))
      

        hilo_rojo.start()
        hilo_verde.start()
        hilo_azul.start()

        
        rojo,termino_rojo,indice_rojo = hilo_rojo.join()
        verde,termino_verde,indice_verde = hilo_verde.join()
        azul,termino_azul,indice_azul = hilo_azul.join()   


        comienzo_rojo = termino_rojo + interleave*9 - size
        comienzo_verde = termino_verde + interleave*9 - size
        comienzo_azul = termino_azul + interleave*9 - size

        escribir(rojo,verde,azul,output)


        if indice_rojo >= len(mensaje_str) and indice_verde >= len(mensaje_str) and indice_azul >= len(mensaje_str):
            print("Se termino de encriptar")
            break
         

    while True:
    
        cuerpo = fd_image.read(size)        

        pixels = [i for i in cuerpo]  

        pixels = array.array('B',pixels) 


        with open(output, 'ab') as f:
            pixels.tofile(f)

        if len(cuerpo) != size:
            break


    print("Finalizado con exito, el proceso tardo: ")
    print(time()-time_i , " segundos")

    fd_image.close()
    