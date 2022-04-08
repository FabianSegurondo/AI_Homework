# clase para definir el objeto grafo
class Graph:

    def __init__(self, edges, n):
        # lista de adyacencia en base a lista de listas
        self.adjList = [[] for _ in range(n)]
 
        # aumentan aristas al graph undireccionado
        for (src, dest) in edges:
            self.adjList[src].append(dest)
            self.adjList[dest].append(src)
 
 
# funcion recursiva para ejecutar el grafo de manera transversal
def BFS(graph, v, checked):
 
    checked[v] = True            # check el node 
    print(v, end=' ')               # print el current node
 
    # repite para cada arista (v, u)
    for u in graph.adjList[v]:
        if not checked[u]:       # si `u` no esta checked
            BFS(graph, u, checked)
 
 #ejemplo
if __name__ == '__main__':
 
    # Lista de aristas de un grafo
    edges = [
        # Notice that node 0 is unconnected
        (1, 2), (1, 7), (1, 8), (2, 3), (2, 6), (3, 4),
        (3, 5), (8, 9), (8, 12), (9, 10), (9, 11)
    ]
 
    # numero de nodes en el grafo
    n = 13
 
    # construir el grafo con las aristas
    graph = Graph(edges, n)
 
    # vistar cada vertice para comprobar si fue checked o no
    checked = [False] * n
 
    # dfs para todos los nodes que no estan checked y llamada recursiva para cubrir todas las aristas y vertices del grafo 
    # cover all connected components of a graph
    for i in range(n):
        if not checked[i]:
            BFS(graph, i, checked)

#complejidad O(n)