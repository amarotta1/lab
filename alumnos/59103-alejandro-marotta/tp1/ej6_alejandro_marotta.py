#6 - Escriba un programa que acepte una serie de números separados por coma, 
# y genere una lista de python ordenada de manera descendente.

def ordenar(lista):
    lista1 = []
   
    for x in lista:
        num = int(x)
        lista1.append(num)
    
    lista1.sort(reverse = True)
    
    return lista1


def crear_lista(string):

    lista = string.split(',')
    return lista

def imprimir(lista):
    print(ordenar(crear_lista(lista)))


valores = input(" Ingrese separado por comas los valores de la lista: ")

imprimir(valores)