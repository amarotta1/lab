# 3 - Rescriba un programa que cree un histograma de una lista de enteros ingresados por teclado.


def crear_histograma(lista,caracter = "*"):
    for x in lista:
        num = int(x)
        print(caracter * num)


def crear_lista(string):

    lista = string.split(',')
    return lista


valores = input(" Ingrese separado por comas los valores del histograma: ")

crear_histograma(crear_lista(valores))
