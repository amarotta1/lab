import sys

def leer(message):

   
    try:        
        fd_message = open(message,"rb")

    except FileNotFoundError:
        print("El archivo no existe")
        print("Intentelo de nuevo")
        sys.exit()

    
    #leo el mensaje y armo una lista con cada caracter
    leido_message = fd_message.read()

    lista_caracteres = []

    for i in leido_message:  #si no lo hago en este formato le pone un 0b adelante, toma valor str
        lista_caracteres.append("{0:b}".format(i))

    #Agrego los ceros mas significativos

    contador = 0

    for caracter in lista_caracteres:
        for i in range(8-(len(caracter))):
            caracter = "0" + caracter
        
        lista_caracteres[contador]= caracter
        contador +=1

    mensaje_str =""
    #finalmente me queda todo el mensaje en ceros y unos como un solo texto
    for caracter in lista_caracteres:
        mensaje_str = mensaje_str + caracter

    longitud = len(leido_message)

    fd_message.close()

    return mensaje_str , longitud