#!/usr/bin/python3

import matplotlib.pyplot as h

def crear_histograma():
    
    
    archivo = open("histograma_texto.txt")

    string = archivo.read()

    lista = string.split(',') 

    print ("Valores leidos: ", lista)

    lista.sort()    

    h.hist(lista, bins = 20)
    h.xticks(range(10))
    h.title("Histograma")
    h.xlabel("Numeros")
    h.ylabel("Veces")
    h.show()

if __name__ == "__main__":
    crear_histograma()



