# 1 - Realize un programa al que se le da un nro (n) por argumento y el resultado será n + nn + nn. 

def num(nro):
    n2= nro*10 + nro
    n3 = nro*100 +nro*10+ nro
    
    return nro+n2+n3

valor = int(input("Ingrese un numero: "))

print(num(valor))


