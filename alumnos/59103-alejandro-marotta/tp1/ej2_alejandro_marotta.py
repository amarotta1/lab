#2 - Modificar el programa anterior, ingresando un segundo nro (m) por argumento,
#  que será el encargado de indicar cuantas sumas se harán.

def num(nro,m):
   
    suma = 0
    valor2 = 0

   
    for x in range (m):
        valor1 = nro* (10**x)
        valor2 = valor2+valor1
        suma = suma+valor2
   
    return suma    
                           


inicio = int(input("Ingrese el numero a iterar: "))
it = int(input("¿Cuantas veces desea iterar?: "))

print(num(inicio,it))      

   

