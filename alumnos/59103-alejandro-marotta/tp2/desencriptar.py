from argparse import ArgumentParser
import array
import re
import sys
import os.path
import time


def parseArguments():

    analizador = ArgumentParser(description='Esteganografía')

    analizador.add_argument("-f","--file",required=True,help = "Imagen ppm a analizar")
    
          

    return analizador.parse_args()


def decode(s):
    print("\n")
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))


def search(cuerpo,interleave):

    mensaje_bin = ""
    contador = 0

    for j in range (0,len(cuerpo),interleave*3):

        if contador ==0 :
            binario = "{0:b}".format(cuerpo[j]) #str

            mensaje_bin = mensaje_bin +  binario[-1]

            contador +=1
                
        elif contador == 1:

            binario = "{0:b}".format(cuerpo[j+1]) #str

            mensaje_bin = mensaje_bin +  binario[-1]

            contador +=1

        elif contador ==2:
            binario = "{0:b}".format(cuerpo[j+2]) #str

            mensaje_bin = mensaje_bin +  binario[-1]

            contador = 0

    return mensaje_bin




if __name__ == "__main__":

    arg = parseArguments()

    f = arg.file    
    

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

    encabezado = leido_imagen[:valor].decode()

    lineas = encabezado.splitlines()

    comentario,offset,interleave,longitud = lineas[1].split()

    offset = int(offset)
    interleave = int(interleave)
    longitud = int(longitud)

        
    fd_image.seek(valor) #vuelvo hasta donde comienza el cuerpo 

    inicio = (offset-1)*3 #leo hasta el pixel anterior del offset donde quiero empezar

    cuerpo = fd_image.read(inicio)

    cuerpo = fd_image.read(longitud*8*interleave*3)


    pixels = [i for i in cuerpo]

    mensaje = search(pixels,interleave)

    print(decode(mensaje))

    fd_image.close()

   



    

    
  