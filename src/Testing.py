
import unittest
from Estados import *
from Mapa import *
from Const import *
from Nodo import *
import ast
import re


class TestLaGomeraFunctions(unittest.TestCase):
    def leerArchivo(self,ruta):
        elementos = []
        with open(ruta, 'r') as archivo:
            for linea in archivo:
                elementos.append(linea.split())
        return elementos
        
    def test_Tarea1(self):
        print("EJECUTANDO TEST TAREA 1")
        mapa=Mapa(FileNameGlobal)
        lineas = self.leerArchivo(ruta_test1_original)
        for elementos in lineas:
            if len(elementos) == 3:
                y_cord, x_cord, result = elementos
                try:
                    y = int(y_cord)
                    x = int(x_cord)
                    result = float(result)
                except ValueError as e:
                    print(f"Error de conversión: {e}")
                resultado_umt = mapa.umt_YX(y, x) 
                self.assertEqual(result, resultado_umt)
                
    def test_Tarea1_300(self):
        print("EJECUTANDO TEST TAREA 1 300")
        mapa=Mapa(FileNameGlobal)
        dirmapa=DirNameResize+"300.hdf5"
        mapa.resize(factor=300,transform=transformacion_media,new_name=dirmapa)
        mapa_resize=Mapa(dirmapa)
        lineas = self.leerArchivo(ruta_test1_300)
        for elementos in lineas:
            if len(elementos) == 3:
                y_cord, x_cord, result = elementos
                try:
                    y = int(y_cord)
                    x = int(x_cord)
                    result = float(result)
                except ValueError as e:
                    print(f"Error de conversión: {e}")
                resultado_umt = mapa_resize.umt_YX(y, x) 
                self.assertAlmostEqual(result, resultado_umt,places=2)
                
    def test_Tarea1_400(self):
        print("EJECUTANDO TEST TAREA 1 400")
        mapa=Mapa(FileNameGlobal)
        dirmapa=DirNameResize+"400.hdf5"
        mapa.resize(400,transform=transformacion_max,new_name=dirmapa)
        mapa_resize=Mapa(dirmapa)
        lineas = self.leerArchivo(ruta_test1_400)
        for elementos in lineas:
            if len(elementos) == 3:
                y_cord, x_cord, result = elementos
                try:
                    y = int(y_cord)
                    x = int(x_cord)
                    result = float(result)
                except ValueError as e:
                    print(f"Error de conversión: {e}")
                resultado_umt = mapa_resize.umt_YX(y, x) 
                self.assertAlmostEqual(result, resultado_umt,places=2)
                
    def test_Tarea2_300(self):
        print("EJECUTANDO TEST TAREA 2 300")
        mapa = Mapa(FileNameGlobal)
        dirmapa=DirNameResize+"300.hdf5"
        mapa.resize(300,transform=transformacion_media,new_name=dirmapa)
        mapa_resize=Mapa(dirmapa)
        altura_maxima=10000
        factor=1
        lineas = self.leerArchivo(ruta_test2_300)
        for elementos in lineas:
            estado=elementos[0]
            y_coord,x_coord = estado[1:-1].split(',')
            estado_actual=Estado(int(y_coord),int(x_coord))
            print(estado_actual)
            sucesores=generar_sucesores(estado_actual,factor,mapa_resize,altura_maxima)
            if len(elementos)-1==0:
                next
            elif len(elementos)-1==len(sucesores):
                for i in range( len(sucesores)):
                    print("Probando: ",str(sucesores[i])," y ", elementos[i+1])
                    tupla = ast.literal_eval(elementos[i+1])
                    direccion=tupla[0]
                    y,x=tupla[1]
                    
                    y_new=sucesores[i].nuevo_estado.y
                    x_new=sucesores[i].nuevo_estado.x
                    longitud,altura=tupla[2]
                    self.assertEqual(direccion,sucesores[i].direccion)
                    self.assertEqual(y,y_new)
                    self.assertEqual(x,x_new)
                    longitud_gen,altura_gen=sucesores[i].longitud_altura
                    self.assertAlmostEqual(longitud,longitud_gen,places=2)
                    self.assertAlmostEqual(altura,altura_gen,places=2)

    def test_Tarea2_400(self):
        print("EJECUTANDO TEST TAREA 2 400")
        mapa=Mapa(FileNameGlobal)
        dirmapa=DirNameResize+"400.hdf5"
        mapa.resize(400,transform=transformacion_max,new_name=dirmapa)
        mapa_resize=Mapa(dirmapa)
        altura_maxima=10000
        factor=1
        lineas = self.leerArchivo(ruta_test2_400)
        for elementos in lineas:
            estado=elementos[0]
            y_coord,x_coord = estado[1:-1].split(',')
            estado_actual=Estado(int(y_coord),int(x_coord))
            print(estado_actual)
            sucesores=generar_sucesores(estado_actual,factor,mapa_resize,altura_maxima)
            if len(elementos)-1==0:
                next
            elif len(elementos)-1==len(sucesores):
                for i in range( len(sucesores)):
                    print("Probando: ",str(sucesores[i])," y ", elementos[i+1])
                    tupla = ast.literal_eval(elementos[i+1])
                    direccion=tupla[0]
                    y,x=tupla[1]
                    
                    y_new=sucesores[i].nuevo_estado.y
                    x_new=sucesores[i].nuevo_estado.x
                    longitud,altura=tupla[2]
                    self.assertEqual(direccion,sucesores[i].direccion)
                    self.assertEqual(y,y_new)
                    self.assertEqual(x,x_new)
                    longitud_gen,altura_gen=sucesores[i].longitud_altura
                    self.assertAlmostEqual(longitud,longitud_gen,places=2)
                    self.assertAlmostEqual(altura,altura_gen,places=2)
                                
    def test_Tarea3(self):
        print("EJECUTANDO TEST TAREA 3")
        dirmapa=DirNameResize+"GomeraZoom300.hdf5"
        mapa=Mapa(dirmapa)

        # Obtén la lista de archivos en el directorio
        archivos = os.listdir(ruta_test3)

        # Itera sobre cada archivo en el directorio
        for archivo in archivos:
            # Crea la ruta completa al archivo
            ruta_archivo = os.path.join(ruta_test3, archivo)

            # Inicializa diccionario para almacenar las variables
            variables = {}
            j=0
            print(f'Probando archivo: {archivo}')
            # Abre el archivo en modo de lectura
            with open(ruta_archivo, 'r') as file:
                
                # Itera sobre las primeras 5 líneas del archivo
                for i in range(5):
                    linea = file.readline().strip()
                    # Divide la línea en nombre de variable y valor de variable
                    nombre_variable, valor_variable = linea.split(':')
                    # Almacena en el diccionario
                    variables[nombre_variable] = valor_variable
                init = ast.literal_eval(variables["init"])
                estado_incial=Estado(init[0],init[1])
                goal = ast.literal_eval(variables["goal"])
                
                estado_final= Estado(goal[0],goal[1])
                problema = Problema(estado_incial, estado_final)
                if variables["strategy"]=="BFS":
                    estrategia=BFS #BFS -> 2 || DFS -> 3 || UCS -> 4 || VORAZ -> 5 || A -> 6
                elif variables["strategy"]=="DFS":
                    estrategia=DFS
                elif variables["strategy"]=="UCS":
                    estrategia = UCS
                tipo= H_MANHATTAN #    H_EUCLIDIANA -> 0 || H_MANHATTAN -> 1
                maxProfundidad=int(variables["max_depth"])
                maxAltura=100
                factor_avance = 1
                sol=AlgoritmoBusqueda(problema = problema, estrategia = estrategia, profundidad_Maxima = maxProfundidad, mapa = mapa, altura_maxima = maxAltura, factor_avance = factor_avance,tipo=tipo)
                # Lee el resto del archivo
                for linea in file:
                    print(f'Probando: {linea}')
                    cadenagen=sol[j]
                    
                    regex = r"\[(\d+)\]\[\(([\d.]+),\s?([\d.]+)\),\((\d+),(\d+)\),(\d+),([A-Za-z]+),(\d+),([\d.]+),([\d.]+)\]"
                    # Usar expresiones regulares para extraer los valores
                    coincidencias_test = re.match(regex, linea)

                    if coincidencias_test:
                        id_test = int(coincidencias_test.group(1))
                        costo1_test = float(coincidencias_test.group(2))
                        costo2_test = float(coincidencias_test.group(3))
                        estado_test = (int(coincidencias_test.group(4)), int(coincidencias_test.group(5)))
                        id_padre_test = int(coincidencias_test.group(6))
                        accion_test = coincidencias_test.group(7)
                        profundidad_test = int(coincidencias_test.group(8))
                        heuristica_test = float(coincidencias_test.group(9))
                        valor_test = float(coincidencias_test.group(10))
                        
                    coincidencias_gen = re.match(regex, cadenagen)
                    if coincidencias_gen:
                        id_gen = int(coincidencias_gen.group(1))
                        costo1_gen = float(coincidencias_gen.group(2))
                        costo2_gen = float(coincidencias_gen.group(3))
                        estado_gen = (int(coincidencias_gen.group(4)), int(coincidencias_gen.group(5)))
                        id_padre_gen = int(coincidencias_gen.group(6))
                        accion_gen = coincidencias_gen.group(7)
                        profundidad_gen = int(coincidencias_gen.group(8))
                        heuristica_gen = float(coincidencias_gen.group(9))
                        valor_gen = float(coincidencias_gen.group(10))
                        print(f'Test: {linea} Gene: {cadenagen}\n')
                        self.assertEqual(id_test, id_gen)
                        self.assertAlmostEqual(costo1_test, costo1_gen, places=2)
                        self.assertAlmostEqual(costo2_test, costo2_gen, places=2)
                        self.assertEqual(estado_test, estado_gen)
                        self.assertEqual(id_padre_test, id_padre_gen)
                        self.assertEqual(accion_test, accion_gen)
                        self.assertEqual(profundidad_test, profundidad_gen)
                        self.assertAlmostEqual(heuristica_test, heuristica_gen, places=2)
                        self.assertAlmostEqual(valor_test, valor_gen, places=2)
                    j+=1
        
    def test_Tarea4(self):
        print("EJECUTANDO TEST TAREA 4")
        dirmapa=DirNameResize+"GomeraZoom300.hdf5"
        mapa=Mapa(dirmapa)

        # Obtén la lista de archivos en el directorio
        archivos = os.listdir(ruta_test4)

        # Itera sobre cada archivo en el directorio
        for archivo in archivos:
            # Crea la ruta completa al archivo
            ruta_archivo = os.path.join(ruta_test4, archivo)
            match = re.search(r'_([a-z]+)\d', archivo)
            if match:
                tipo = match.group(1)
            else:
                print(f"El archivo {archivo} no contiene un tipo válido.")
            

            # Inicializa diccionario para almacenar las variables
            variables = {}
            j=0
            print(f'Probando archivo: {archivo}')
            # Abre el archivo en modo de lectura
            with open(ruta_archivo, 'r') as file:
                # Itera sobre las primeras 5 líneas del archivo
                for i in range(5):
                    linea = file.readline().strip()
                    # Divide la línea en nombre de variable y valor de variable
                    nombre_variable, valor_variable = linea.split(':')
                    # Almacena en el diccionario
                    variables[nombre_variable] = valor_variable
                init = ast.literal_eval(variables["init"])
                estado_incial=Estado(init[0],init[1])
                goal = ast.literal_eval(variables["goal"])
                
                estado_final= Estado(goal[0],goal[1])
                problema = Problema(estado_incial, estado_final)
                if variables["strategy"]=="BFS":
                    estrategia=BFS 
                elif variables["strategy"]=="DFS":
                    estrategia=DFS
                elif variables["strategy"]=="UCS":
                    estrategia = UCS
                elif variables["strategy"]=="A*":
                    estrategia = A
                elif variables["strategy"]=="GREEDY":
                    estrategia = VORAZ
                if tipo=="euclidea":
                    tipo_h=H_EUCLIDIANA    
                elif tipo=="manhattan":
                    tipo_h=H_MANHATTAN
                maxProfundidad=int(variables["max_depth"])
                maxAltura=100
                factor_avance = 1
                sol=AlgoritmoBusqueda(problema = problema, estrategia = estrategia, profundidad_Maxima = maxProfundidad, mapa = mapa, altura_maxima = maxAltura, factor_avance = factor_avance,tipo=tipo_h)
                # Lee el resto del archivo
                for linea in file:
                    cadenagen=sol[j]
                    #print(cadenagen)
                    #print(linea)
                    regex = r"\[(\d+)\]\[\(([\d.]+),\s?([\d.]+)\),\((\d+),(\d+)\),(\d+),([A-Za-z]+),(\d+),([\d.]+),([\d.]+)\]"
                    # Usar expresiones regulares para extraer los valores
                    coincidencias_test = re.match(regex, linea)

                    if coincidencias_test:
                        id_test = int(coincidencias_test.group(1))
                        costo1_test = float(coincidencias_test.group(2))
                        costo2_test = float(coincidencias_test.group(3))
                        estado_test = (int(coincidencias_test.group(4)), int(coincidencias_test.group(5)))
                        id_padre_test = int(coincidencias_test.group(6))
                        accion_test = coincidencias_test.group(7)
                        profundidad_test = int(coincidencias_test.group(8))
                        heuristica_test = float(coincidencias_test.group(9))
                        valor_test = float(coincidencias_test.group(10))
                        
                    coincidencias_gen = re.match(regex, cadenagen)

                    if coincidencias_gen:
                        id_gen = int(coincidencias_gen.group(1))
                        costo1_gen = float(coincidencias_gen.group(2))
                        costo2_gen = float(coincidencias_gen.group(3))
                        estado_gen = (int(coincidencias_gen.group(4)), int(coincidencias_gen.group(5)))
                        id_padre_gen = int(coincidencias_gen.group(6))
                        accion_gen = coincidencias_gen.group(7)
                        profundidad_gen = int(coincidencias_gen.group(8))
                        heuristica_gen = float(coincidencias_gen.group(9))
                        valor_gen = float(coincidencias_gen.group(10))
                        print(f'Test: {linea} Gene: {cadenagen}\n')
                        self.assertEqual(id_test, id_gen)
                        self.assertAlmostEqual(costo1_test, costo1_gen,places=2)
                        self.assertAlmostEqual(costo2_test, costo2_gen,places=2)
                        self.assertEqual(estado_test, estado_gen)
                        self.assertEqual(id_padre_test, id_padre_gen)
                        self.assertEqual(accion_test, accion_gen)
                        self.assertEqual(profundidad_test, profundidad_gen)
                        self.assertAlmostEqual(heuristica_test, heuristica_gen,places=2)
                        self.assertAlmostEqual(valor_test, valor_gen,places=2)
                    j+=1
        
        
        
        
if __name__ == '__main__':
    
    testing= TestLaGomeraFunctions()
    #testing.test_Tarea1()
    testing.test_Tarea1_300()
    testing.test_Tarea1_400()
    testing.test_Tarea2_300()
    testing.test_Tarea2_400()
    testing.test_Tarea3()
    testing.test_Tarea4()
    print("TEST PASADOS CORRECTAMENTE")