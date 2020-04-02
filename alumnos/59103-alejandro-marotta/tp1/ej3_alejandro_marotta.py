#!/usr/bin/python3

import matplotlib.pyplot as h

def crear_histograma():
    datos = []
    valor = ""
    i = 0
    mayor = 0
    
    while True:
        valor = input("Ingrese un valor entero (o S para salir): ")
        if valor != "S":
            datos.append(valor)
            i+=1
            if int(valor) > mayor:
                mayor = int(valor)
        else:
            print ("Saliendo...")
            break
    
    print("Valores ingresados: ", datos)

    h.hist(datos, bins = 20)
    h.xticks(range(0,(mayor+1)))
    h.title("Histograma")
    h.xlabel("Numeros")
    h.ylabel("Veces")
    h.show()

if __name__ == "__main__":
    crear_histograma()

