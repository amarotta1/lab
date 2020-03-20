# 5 - Describa como funciona el programa siguiente:

def fibo(n,a=0,b=1): #define una funcion "fibo" , la cual recibe "n" como parametro y a los paremetros "a" y "b"
                    # le da valores iniciales 0 y 1

   while n!=0: #mientras que n sea distinto de cero

      return fibo(n-1,b,a+b) #devuelve la funcion de manera recursiva restandole un valor a "n" 
                             #pasando el valor de "b" como parametro de "a" y el valor "a+b" al parametro "b"
                             #lo cual provoca que se vayan sumando los numeros anteriores

   return a #retorna el valor de "a" el cual seria al salir de la sentencia while el valor resultante de la suma
   #de todos los numeros anteriores que se generan con la recursividad
            


for i in range(0,10): 

   print(fibo(i))  #le pasa 10 valores numericos a la funcion fibo, por lo tanto imprime en pantalla los 10
                    #primeros numeros de la funcion fibonacci