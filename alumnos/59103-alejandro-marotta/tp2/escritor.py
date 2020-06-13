import array

def escribir(rojo,verde,azul,nombre):

    pixels = []

    for i in range(0,(len(rojo)-2),3):
        pixels.append(rojo[i])
        pixels.append(verde[i+1])
        pixels.append(azul[i+2]) 

    pixels = array.array('B',pixels) 
    
    #wb es para escribir y ab para hacer un append
    with open(nombre, 'ab') as f:
        pixels.tofile(f)