import sys

def control(encabezado,interleave,longitud,offset):

    lista = encabezado.splitlines()

    for i in lista:
        if "#" in i:
            lista.remove(i)

    largo,ancho = lista[1].split()

    pixels_totales = int(largo)*int(ancho)

    pixels_necesarios = interleave * 8 * longitud + offset

    print("Esta imagen tiene {} pixels".format(pixels_totales))
    print("Se requieren {} pixels para encriptar este mensaje".format(pixels_necesarios))

    if pixels_necesarios > pixels_totales:
        print("ERROR, se necesitan mas pixels de los que tiene esta imagen")
        sys.exit()

