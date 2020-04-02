#!/usr/bin/python3 

import sys

def num(nro,m):
    resultado = 0
    for i in range(1,int(m)+1):
        a = str(nro) * i
        resultado = resultado + int(a)
    
    return resultado

if __name__ == "__main__":

    if (len(sys.argv) == 3):
        print("Con el argumento ",str(sys.argv[1]) ," y la cantidad de veces ", str(sys.argv[2])," el resultado es ", str(num(sys.argv[1],sys.argv[2])))
    else:
        print("Debe ingresar dos argumentos")
    
       

   

