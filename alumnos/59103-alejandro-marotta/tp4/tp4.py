import asyncio
from argparse import ArgumentParser
from aiofile import AIOFile
import os
from datetime import datetime

async def parseArguments():

    analizador = ArgumentParser(description='Entrada al Servidor')
    
    analizador.add_argument("-p","--port",type=int,default=5000,help = "Puerto donde se espera la conexion")
    analizador.add_argument("-d","--documentroot",required=True,help = "Directorio donde se encuantran los documentos web")
    analizador.add_argument("-s","--size",type=int,default=1026,help = "Bloque de lectura, debe ser multiplo de 3") 
    
    return analizador.parse_args() 


async def handler(reader,writer):

    data = await reader.read(1024)
    addr = writer.get_extra_info('peername')
    encabezado = ""

    try:
        encabezado = data.decode().splitlines()[0] #solo necesito la primer linea
        archivo = encabezado.split()[1] #el texto en la posicion 1 es /archivo.ext; 
        if archivo == '/':
            archivo = '/index.html'
    except:
        archivo = '/index.html'

    codigo = "200 OK"

  
    t1 =  asyncio.create_task(abrir_archivos(archivo,writer,codigo))
    t2 = asyncio.create_task(registro(addr,encabezado,archivo))
   
    await t1
    await t2



async def abrir_archivos(archivo,writer,codigo):

    arg = await parseArguments()
    root = arg.documentroot
    size = arg.size   

    archivo = root + archivo

    try:
      fd = open(archivo,"rb")
      await escritura(archivo,fd,writer,codigo,size)
    
    except FileNotFoundError:
        archivo = "/error.html"
        codigo = "404 Not Found"
        await abrir_archivos(archivo,writer,codigo)

    except:
        archivo = '/500.html'
        codigo = "500 Internal server error"
        await abrir_archivos(archivo,writer,codigo)
    
async def escritura(archivo,fd,writer,codigo,size):

    dic ={".txt":" text/plain",".jpg":" image/jpeg",".ppm":" image/x-portable-pixmap",".html":" text/html",".pdf":" application/pdf"}

    extension = os.path.splitext(archivo)[1]
    header = bytearray("HTTP/1.1 "+codigo+"\r\nContent-type:"+ dic[extension] +"\r\nContent-length:"+str(os.path.getsize(archivo))+"\r\n\r\n","utf8")

    writer.write(header)
    await writer.drain()

    
    while True:
        data = fd.read(size)
        writer.write(data)                        
        if len(data) != size:
            break
    
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def registro(addr,encabezado,archivo):
    async with AIOFile("registro.txt","a") as f: #escritura asincrona, bajo medio segundo el tiempo
        cliente = "Cliente: {}\nPeticion: {}\nArchivo:{}\nFecha: {}\n\n".format(addr,encabezado,archivo,datetime.now())
        await f.write(cliente)
        await f.fsync()


async def main():

    arg = await parseArguments()
    port = arg.port

    """
    server = await asyncio.start_server(
        handler, ['::1','127.0.0.1'], port)"""

    server = await asyncio.start_server(
        handler, '127.0.0.1', port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())


