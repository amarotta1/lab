#!/usr/bin/python3
import socketserver
import os
from argparse import ArgumentParser
import ppm
import pickle
import array
from concurrent import futures

def parseArguments():

    analizador = ArgumentParser(description='Entrada al Servidor')
    
    analizador.add_argument("-p","--port",type=int,default=5000,help = "Puerto donde se espera la conexion")
    analizador.add_argument("-d","--documentroot",required=True,help = "Directorio donde se encuantran los documentos web")
    analizador.add_argument("-s","--size",type=int,default=1026,help = "Bloque de lectura, debe ser multiplo de 3") 
    
    return analizador.parse_args() 



class Handler(socketserver.BaseRequestHandler):

    def handle(self):

        arg = parseArguments()

        self.root = arg.documentroot        
        self.size = arg.size

        while (self.size%3 != 0):
            self.size += 1 

        
        self.dic ={".txt":" text/plain",".jpg":" image/jpeg",".ppm":" image/x-portable-pixmap",".html":" text/html",".pdf":" application/pdf"}
        
        self.data = self.request.recv(1024)

        print("CLIENTE: ",self.client_address)
        print("PETICION: ",self.data.decode())
        print()
        
        try:
            encabezado = self.data.decode().splitlines()[0] #recibe un texto largo del get, yo solo necesito la primer linea
            self.archivo = encabezado.split()[1] #el texto en la posicion 1 es /archivo.ext; 
        except:
            self.archivo = '/'

        self.codigo = ""
        
              
        if "?" in self.archivo:
            self.archivos_ppm()
        
        elif self.archivo == '/':#si esta vacio
            self.index() #agregar si try except para que se abra el error
       
        else:
            self.abrir_archivos()         
                

                  
      
    def escritura(self,codigo,extension):
        header = bytearray("HTTP/1.1 "+codigo + "\r\nContent-type:"+ self.dic[extension] +"\r\nContent-length:"+str(os.path.getsize(self.archivo))+"\r\n\r\n",'utf8')
        
        self.request.sendall(header) 
        
        while True: 
            body = self.fd.read(self.size)
            self.request.sendall(body)

            if len(body) != self.size:
                break

    
    def index(self):
        self.archivo = self.root + '/index.html'
        self.fd = open(self.archivo,"rb") #si no existe larga FileNotFound
        self.extension = os.path.splitext(self.archivo)[1]
        self.codigo = "200 OK"

        self.escritura(self.codigo,self.extension)

        self.fd.close()

    def error(self):
        self.archivo = self.root + "/error.html"  #CUIDADO,me queda como la extension del archivo anterior
        self.fd = open(self.archivo,"rb") #si no existe larga FileNotFound
        self.extension = os.path.splitext(self.archivo)[1]
        self.codigo = "404 Not Found"

        self.escritura(self.codigo,self.extension)

        self.fd.close()

    def error_500(self):
        self.archivo = self.root + '/500.html'
        self.fd = open(self.archivo,"rb") #si no existe larga FileNotFound
        self.extension = os.path.splitext(self.archivo)[1]
        self.codigo = "500 Internal server error"

        self.escritura(self.codigo,self.extension)

        self.fd.close()
        

    def abrir_archivos(self):
        try:
            self.archivo = self.root + self.archivo
            self.fd = open(self.archivo,"rb") #si no existe larga FileNotFound
            self.extension = os.path.splitext(self.archivo)[1]
            self.codigo = "200 OK"

            self.escritura(self.codigo,self.extension)

            self.fd.close()
            
        except FileNotFoundError:
            self.error()
        except:
            self.error_500()

    def archivos_ppm(self):          
        try:
            self.archivo,parametros = self.archivo.split("?")
            self.archivo = self.root+self.archivo

            self.extension = os.path.splitext(self.archivo)[1]

            if self.extension != ".ppm":
                raise Warning

            
            filtro,escala = parametros.split("&")
            filtro = filtro.split("=")[1]
            escala = escala.split("=")[1] 
            escala = float(escala) #si meto cualquier cosa larga un error que es capturado

            if (filtro!="rojo" and filtro!="verde" and filtro!="azul" and filtro!="BN"):
                raise Warning


            self.codigo = "200 OK"

            self.fd = open(self.archivo,"rb") #Si no lo encuentra larga FileNotFoundError
            

            header = bytearray("HTTP/1.1 "+self.codigo + "\r\nContent-type:"+ self.dic[self.extension] +"\r\nContent-length:"+str(os.path.getsize(self.archivo))+"\r\n\r\n",'utf8')
            
            self.request.sendall(header) 

            ppm_encab = ppm.encabezado(self.fd)

            self.request.sendall(ppm_encab)

            rango = round(os.path.getsize(self.archivo)/self.size)+1  

            #valores = ((self.fd,filtro,escala,self.size),)*rango

        
            hilos = futures.ThreadPoolExecutor(max_workers=rango)
            resultado_a_futuro = hilos.map(ppm.selector ,(self.fd,)*rango,(filtro,)*rango,(escala,)*rango,(self.size,)*rango)                   
            
            for r in resultado_a_futuro:
                self.request.sendall(bytearray(r))

            self.fd.close()

        except FileNotFoundError:
            self.error()
        
        except:
            self.error_500()
            
        
#HAY QUE CERRAR LOS ARCHIVOS        
           
if __name__ == "__main__":

    arg = parseArguments()
    port = arg.port
    
    socketserver.TCPServer.allow_reuse_address = True
    server =  socketserver.TCPServer(("0.0.0.0", port), Handler)
    server.serve_forever()