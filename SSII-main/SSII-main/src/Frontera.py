import heapq

class Frontera:
    def __init__(self):
        self.frontera = []


    def insertar(self, nodo):
        heapq.heappush(self.frontera, (nodo.valor, nodo.id, nodo))

    def tomar_nodo(self):
        if self.frontera:
            return heapq.heappop(self.frontera)[2]
        else:
            return None
        
    def contiene(self, nodo):
        return nodo in self.frontera
    
    def es_vacia(self):
        return not self.frontera
