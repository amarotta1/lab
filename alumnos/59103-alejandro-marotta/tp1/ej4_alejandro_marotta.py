# 4 - Modificar el ejercicio anterior para leerlo de un archivo.


archivo = open("histograma_texto.txt")



def crear_histograma(lista,caracter = "*"):
    for x in lista:
        num = int(x)
        print(caracter * num)


def crear_lista(string):

    lista = string.split(',')
    return lista


valores = archivo.read()

crear_histograma(crear_lista(valores))
