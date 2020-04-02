#!/usr/bin/python3 

import sys

def num(nro):
    resultado = 0
    for i in range(1,4):
        a = str(nro) * i
        resultado = resultado + int(a)
    
    return resultado

if __name__ == "__main__":
    
    print("Con el argumento ",str(sys.argv[1]) , " el resultado es ", str(num(sys.argv[1])))

