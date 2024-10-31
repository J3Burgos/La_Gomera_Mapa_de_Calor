from Mapa import *
from Estados import *
from Frontera import *


class Problema:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        Nodo.total_nodos=0

    def objetivo(self, estado):
        return estado.equals(self.estado_final)

class Nodo:
    total_nodos=0 # Contador global para IDs de nodos
    
    def __init__(self, padre, estado, valor, profundidad, costo, heuristica, accion):
        self.id = Nodo.total_nodos
        Nodo.total_nodos += 1
        self.padre = padre
        self.estado = estado
        self.valor = valor
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = heuristica
        self.accion = accion

    def camino(self):
        if self.padre is None:
            return [self]
        else:
            return self.padre.camino() + [self]
        
    def calcular_valor(self, estrategia,tipo, estado_final=None):
        # Calcula la heurística independientemente de la estrategia
        self.heuristica=0
        if estrategia==VORAZ or estrategia==A:
            if tipo==H_EUCLIDIANA:
                self.heuristica = heuristica_euclidiana(self.estado, estado_final)  # heuristica_euclidiana o heuristica_manhattan
            else:
                self.heuristica = heuristica_manhattan(self.estado, estado_final)
                
        if estrategia == BFS:
            return self.profundidad 
        elif estrategia == DFS:
            return 1 / (self.profundidad + 1) 
        elif estrategia == UCS:
            return self.costo[0]
        elif estrategia == VORAZ:
            return self.heuristica
        elif estrategia == A:
            return self.costo[0] + self.heuristica


    def __str__(self):
        costo_str = "({:.3f}, {:.3f})".format(self.costo[0], self.costo[1])
        valor_str = "{:.3f}".format(self.valor)
        return f"[{self.id}][{costo_str},{self.estado},{self.padre.id if self.padre else None},{ self.accion.direccion if self.accion else None},{self.profundidad},{self.heuristica},{valor_str}]"

class ConjuntoVisitados:
    def __init__(self):
        self.visitados = set()

    def pertenece(self, estado):
        return (estado.y, estado.x) in self.visitados

    def insertar(self, estado):
        self.visitados.add((estado.y, estado.x))



def AlgoritmoBusqueda(problema, estrategia, profundidad_Maxima, mapa, altura_maxima, factor_avance,tipo):
    nodos_generados=0
    frontera = Frontera()
    visitados = ConjuntoVisitados()
    n_inicial = Nodo(None, problema.estado_inicial, 0.0, 0, (0,0), None, Accion("",None,None))
    n_inicial.valor = n_inicial.calcular_valor(estrategia=estrategia, estado_final=problema.estado_final,tipo=tipo)
    frontera.insertar(n_inicial)
    #### EXPANDIDOS-PODADOS-FRONTERA ####
    expandidos = 0
    n_frontera = 0
    podados = 0
    #### EXPANDIDOS-PODADOS-FRONTERA ####
    #### PRIMOS ####
    padre_b = None
    abuelo_b = None
    #### PRIMOS ####
    while not frontera.es_vacia():
        n_actual = frontera.tomar_nodo()
        
        #### ID DEL ULTIMO NODO VISITADO EN EL ESTADO (Y,X) ####
        estado_a_buscar = Estado(y=3120161,x=278453)
        if n_actual.estado.y==estado_a_buscar.y and n_actual.estado.x==estado_a_buscar.x:
            print(n_actual)
        #### ID DEL ULTIMO NODO VISITADO EN EL ESTADO (Y,X) ####
        
        #### ABUELO ####
        id = 400000
        if n_actual.id==id:
            print("ID=136: ", n_actual)
            padre=n_actual.padre
            print("PADRE: ", padre)
            abuelo=padre.padre
            print("ABUELO: ", abuelo)      
        #### ABUELO ####

        #### PRIMOS ####
        id_b = 400000
        if n_actual.id==id_b:
            padre_b=n_actual.padre
            abuelo_b=padre_b.padre
        if padre_b != None or abuelo_b != None: ## Si no es None, entonces si tiene padre y abuelo
            if n_actual.padre.padre == abuelo_b and n_actual.padre != padre_b:
                print("PRIMO: ", n_actual)
        #### PRIMOS ####

        if problema.objetivo(n_actual.estado):
            ##### NODOS FRONTERA ####
            while not frontera.es_vacia():
                nodo_frontera=frontera.tomar_nodo()
                if nodo_frontera.accion.direccion=="NE":
                    n_frontera+=1

            resultF=n_frontera-podados
            print(f'Resultado n_frontera-podados: {resultF}')    
            ##### NODOS FRONTERA ####

            ##### EXPANDIDOS-PODADOS ####
            result=expandidos-podados
            print(f'Resultado expandidos-podados: {result}')
            #### EXPANDIDOS-PODADOS ####
            return CrearSolucion(n_actual)
        
        if n_actual.profundidad > profundidad_Maxima or visitados.pertenece(n_actual.estado):
            #### NODOS PODADOS ####
            if n_actual.accion.direccion=="NE":
                podados+=1
            #### NODOS PODADOS ####
            continue    
      
        
        visitados.insertar(n_actual.estado)
        lista_suc = generar_sucesores(n_actual.estado, factor_avance, mapa, altura_maxima)
        
        #### NODOS EXPANDIDOS ####
        if n_actual.accion.direccion=="NE":
            expandidos+=1
        #### NODOS EXPANDIDOS ####
        
        for accion in lista_suc:
            nuevo_nodo = CrearNodo(accion=accion, nodo_padre=n_actual, estrategia=estrategia, estado_final=problema.estado_final,tipo=tipo)                      
            nodos_generados+=1
            frontera.insertar(nuevo_nodo)
        
    print(nodos_generados)
    return "No hay solución"

def CrearNodo(accion, nodo_padre, estrategia, estado_final,tipo):
    distancia_padre, altura_padre = nodo_padre.costo
    distancia_hijo, altura_hijo = accion.longitud_altura
    distancia_total = distancia_padre + distancia_hijo
    altura_total = max(altura_padre, altura_hijo) 

    nuevo_nodo = Nodo(padre=nodo_padre,estado=accion.nuevo_estado,valor=0,costo=(distancia_total,altura_total) ,accion=accion, profundidad=nodo_padre.profundidad + 1,heuristica=0)
    nuevo_nodo.valor = nuevo_nodo.calcular_valor(estrategia=estrategia, estado_final=estado_final,tipo=tipo)
    return nuevo_nodo


def CrearSolucion(nodo):
    camino_solucion = nodo.camino()
    return [str(n) for n in camino_solucion]

def heuristica_euclidiana(estado, estado_final):
    return math.sqrt((estado_final.x - estado.x)**2 + (estado_final.y - estado.y)**2)

def heuristica_manhattan(estado, estado_final):
    return abs(estado_final.x - estado.x) + abs(estado_final.y - estado.y)

if __name__ == '__main__':
    
    mapa=Mapa(FileNameGlobal)
    name_reszie_map=DirNameResize+"Gomerazoom140.hdf5"
    mapa_resize = mapa.resize(factor=140, transform=transformacion_media,new_name=name_reszie_map)
    #mapa_resize=Mapa("Maps_Resize/300.hdf5")
    estado_incial=Estado(3109681, 270733)
    estado_final= Estado(3115281, 291733)
    problema = Problema(estado_incial, estado_final)
    estrategia = 6       #BFS(altura) -> 2 || DFS(Profundidad) -> 3 || UCS -> 4 || VORAZ -> 5 || A -> 6
    tipo = 0             #H_EUCLIDIANA -> 0 || H_MANHATTAN -> 1
    maxProfundidad=500000   #500000
    maxAltura=447
    factor_avance = 1
    sol=AlgoritmoBusqueda(problema = problema, estrategia = estrategia, profundidad_Maxima = maxProfundidad, mapa = mapa_resize, altura_maxima = maxAltura, factor_avance = factor_avance,tipo=tipo)
    print("\nSOLUCION: ")
    for s in sol:
        print(s)
