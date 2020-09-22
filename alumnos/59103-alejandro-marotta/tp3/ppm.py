import array
import re

def encabezado(fd):

    leido_imagen = fd.read(150)

    for c in re.finditer(b'\n', leido_imagen):
    
        valor = c.end()

    encabezado = leido_imagen[:valor].decode()
      
    fd.seek(valor)

    return bytearray(encabezado, 'ascii')

def selector(fd,color,escala,size):

    cuerpo = fd.read(size)

    pixels = [i for i in cuerpo] 


    if color == "azul":
        return azul(pixels,escala)            

    elif color == "rojo": 
        return rojo(pixels,escala)

    elif color == "verde":
        return verde(pixels,escala)
    
    elif color == "BN":
        return blancoNegro(pixels,escala)
        


def blancoNegro(pixels,escala):

    bn = []

    for j in range(0,len(pixels),3):
        
        promedio = pixels[j]+pixels[j+1]+pixels[j+2]
        promedio = promedio/3        
        
        valor = round(promedio*escala)
        if valor > 255:
            valor = 255
    
        bn.append(valor)
        bn.append(valor)
        bn.append(valor)
    
    return bn


def rojo(pixels,escala):

    rojo = []   
                      
    for j in range(0,len(pixels),3):
        valor = pixels[j]
        valor = round(valor*escala)
        if valor > 255:
            valor = 255
    
        rojo.append(valor)
        rojo.append(0)
        rojo.append(0)
    
    return rojo

def azul(pixels,escala):

    blue = []               

    for j in range(2,len(pixels),3):
        valor = pixels[j]
        valor = round(valor*escala)
        if valor > 255:
            valor = 255
        
        blue.append(0)
        blue.append(0)
        blue.append(valor)    

    return blue
    

def verde(pixels,escala):

    green = []        

    for j in range(1,len(pixels),3):
        valor = pixels[j]
        valor = round(valor*escala)
        if valor > 255:
            valor = 255
        green.append(0)
        green.append(valor)
        green.append(0)

    return green
