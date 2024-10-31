# Ruta del archivo HDF5
from Const import *
from Mapa import *

class Estado:
    def __init__(self, y, x):
        self.y = y
        self.x = x
    def gety(self):
        return self.y
    def getx(self):
        return self.x
    def equals(self, otro_estado):
        return self.x == otro_estado.x and self.y == otro_estado.y
    def __str__(self):
        return f"({self.y},{self.x})"

class Accion:
    def __init__(self, direccion, nuevo_estado, longitud_altura):
        self.direccion = direccion
        self.nuevo_estado = nuevo_estado
        self.longitud_altura = longitud_altura

    def __str__(self):
        return f"({self.direccion},{self.nuevo_estado},{self.longitud_altura})"

def generar_sucesores(estado, factor_avance, mapa, altura_maxima):
    sucesores = []
    ################################################################################
    ####################### ['N', 'E', 'SE', 'S', 'O', 'NO'] #######################
    ################# ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO'] #################
    ################################################################################
    direcciones = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
    for direccion in direcciones:
        if direccion == 'N':
            nuevo_estado = Estado(estado.y + factor_avance * mapa.size_cell, estado.x)
        elif direccion == 'NE':
            nuevo_estado = Estado(estado.y + factor_avance * mapa.size_cell, estado.x + factor_avance * mapa.size_cell)
        elif direccion == 'E':
            nuevo_estado = Estado(estado.y, estado.x + factor_avance * mapa.size_cell)
        elif direccion == 'SE':
            nuevo_estado = Estado(estado.y - factor_avance * mapa.size_cell, estado.x + factor_avance * mapa.size_cell)
        elif direccion == 'S':
            nuevo_estado = Estado(estado.y - factor_avance * mapa.size_cell, estado.x)
        elif direccion == 'SO':
            nuevo_estado = Estado(estado.y - factor_avance * mapa.size_cell, estado.x - factor_avance * mapa.size_cell)
        elif direccion == 'O':
            nuevo_estado = Estado(estado.y, estado.x - factor_avance * mapa.size_cell)
        elif direccion == 'NO':
            nuevo_estado = Estado(estado.y + factor_avance * mapa.size_cell, estado.x - factor_avance * mapa.size_cell)

        if direccion =="NO" or direccion == "NE" or direccion == "SE" or direccion == "SO":
            longitud = float(math.sqrt(2)*mapa.size_cell*factor_avance)
        else:
            longitud = float( factor_avance * mapa.size_cell)

        altura = abs(mapa.umt_YX(estado.y,estado.x) - mapa.umt_YX(nuevo_estado.y,nuevo_estado.x))
        
        accion = Accion(direccion, nuevo_estado, (longitud, altura))
        
        if altura<=altura_maxima:
            sucesores.append(accion)

    return sucesores


if __name__ == "__main__":  
    estado_actual = Estado(y=3101029,x=278933)
    factor_desplazamiento = 1  # Ajustar según sea necesario
    altura_maxima=10000

    mapa = Mapa(FileNameGlobal)

    name_reszie_map=DirNameResize+"400.hdf5"
    mapa_resize = mapa.resize(factor=400, transform=transformacion_max,new_name=name_reszie_map)
    #mapa_resize=Mapa("Maps_Resize/300.hdf5")
    
    sucesores = generar_sucesores(estado_actual,factor_desplazamiento, mapa_resize, altura_maxima)
    print(mapa_resize.size_cell)

    for sucesor in sucesores:
        print(sucesor)


