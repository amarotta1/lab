
def esteganografo(mensaje,cuerpo,comienzo_mensaje,comienzo_cuerpo,interleave):

    
    indice = comienzo_mensaje
    termino = 0

    for j in range (comienzo_cuerpo,len(cuerpo),interleave*9):

        if indice > (len(mensaje)-1):
            break

        binario = "{0:b}".format(cuerpo[j]) #str
        binario = binario[0:-1]+(mensaje[indice])
        cuerpo[j] = int(binario, 2) #lo pongo en base 2

        termino = j  #ultima posicion que edito del cuerpo
        indice +=3 #ultima posicion que edito del mensaje
    
    return cuerpo,termino,indice

