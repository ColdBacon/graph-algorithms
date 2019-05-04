import random
from random import randint

class Edge():
    def __init__(self, source, target, weight = 1):     #inicjalizuje obiekt krawędzi
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):                     #krawędź jako tekst
        if self.weight == 1:
            return "Edge(%s, %s)" % (repr(self.source), repr(self.target))
        else:
            return "Edge(%s, %s, %s)" % (repr(self.source), repr(self.target), repr(self.weight))

    def __hash__(self):                     #zwraca hash dla krawędzi(niezmienialność, żeby można włożyć jako key do słownika)
        return hash(repr(self))


class Graph(dict):
    def __init__(self, n=0, directed = False):  #inicjalizuje obiekt grafu
        self.n = n
        self.directed = directed
        self.edges = []

    def is_directed(self):                  #sprawdza czy graf jest skierowany
        return self.directed

    def v(self):                            #zwraca liczbę V grafu
        return len(self)

    def e(self):                            #zwraca liczbę E grafu
        edges = sum( len(self[node]) for node in self)
        return ( edges if self.is_directed() else edges/2 )

    def add_node(graph, node):              #dodaje wierczhołek
        if node not in graph:
            graph[node]={}

    def has_node(self, node):               #sprawdza czy V należy do grafu
        return node in self

    def del_node(self, node):               #usuwa V
        for edge in list(self.iterinedges(node)):
            self.del_edge(edge)
        if self.is_directed():
            for edge in list(self.iteroutedges(node)):
                self.del_edge(edge)
        del self[node]

    def add_edge(self, edge):               #dodaje E
        if edge.source == edge.target:
            raise ValueError("pętle są zabronione(1)")
        self.add_node(edge.source)
        self.add_node(edge.target)
        self.edges.append(edge)
        if edge.target not in self[edge.source]:
            self[edge.source][edge.target] = edge.weight
        if not self.is_directed():
            if edge.source not in self[edge.target]:
                self[edge.target][edge.source] = edge.weight

    def del_edge(self, edge):               #usuwa E
        del self[edge.source][edge.target]
        
    def has_edge(self, edge):               #sprawdza, czy krawędź istnieje
        return edge.source in self and edge.target in self[edge.source]
        
    def iternodes(self):                    #zwraca iterator do listy V
        return self.keys()

    def iteradjacent(self, source):         #zwraca iterator V sąsiednich
        return self[source].keys()

    def iterinedges(self, source):          #zwraca iterator E wchodzących
        if self.is_directed():
            for(target, sources_dict) in self.iteritems():
                if source in sources_dict:
                    yield Edge(target, source, sources_dict[source])
        else:
            for target in self[source]:
                yield Edge(target, source, self[target][source])

    def iteroutedges(self, source):         #zwraca iterator E wychodzących
        for target in self[source]:
            yield Edge(source, target, self[source][target])

    def show(self):                         #prezentacja grafu
        for source in self.iternodes():
            print(source, ":")
            for edge in self.iteroutedges(source):
                print("%s(%s)" %(edge.target, edge.weight))

def random_edges(graph, n):
    full = n*(n-1)/2
    m = int(full * 0.6)
    vout = list()                           #lista wychodzących
    vin = list()                            #lista wchodzących
    
    for i in range(1, m+1):
        j = random.randint(1, n-1)
        k = random.randint(j+1, n)
        while graph.has_edge(Edge(j, k)):
            j = random.randint(1, n-1)
            k = random.randint(j+1, n)
        weight = random.randint(1,1000)
        graph.add_edge(Edge(j, k, weight))
        if j not in vout:
            vout.append(j)                  
        if k not in vin:
            vin.append(k)
            
    for i in graph.iternodes():             #sprawdzam spójność grafu
        if i not in vout and i not in vin:
            j=1
            while len(graph[j]) <= 1:
                j+=1
            key_list = list()
            for k in graph[j].keys():
                key_list.append(k)
            graph.del_edge(Edge(graph[j], graph[key_list[-1]]))
            new = random.randint(i+1, n)
            weight = random.randint(1000)
            graph.add_edge(Edge(i, new, weight))
    
    return graph

def MST(graph,n):
    TV=[1] #wierzcholki w drzewie -> 1 wierzcholek startowy
    T=[] #krawedzie w drzewie -> na start lista pusta
    edges = graph.edges
    MST = Graph()
    while len(T)<n-1:
        min = 1001
        tmpu=n+1
        tmpv=n+1
        for u in TV:
            for v in graph.iteradjacent(u):
                if graph[u][v]<min and ((v in TV)==False):
                    min=graph[u][v]
                    tmpu=u
                    tmpv=v
                    
        if min==1001:
            break
        else:
            TV.append(tmpv)
            T.append([tmpu,tmpv,min])
    return T
    
def primMST(graph, startVertex, n):
    cost = 0

    visited = [ startVertex ]
    notvisited = list(range(1, n+1, 1))
    edges = graph.edges
    isSpanAllVertices = False

    # List to store minimum spanning tree
    minimumSpanningTree = Graph()

    while isSpanAllVertices == False:
        isSpanAllVertices = True

        cutEdges = []

        for edge in edges:
            if edge.source in visited and edge.target in notvisited:
                isSpanAllVertices = False
                cutEdges.append( Edge(source = edge.source, target = edge.target, weight = edge.weight) )

            elif edge.source in notvisited and edge.target in visited:
                isSpanAllVertices = False
                cutEdges.append( Edge(source = edge.target, target = edge.source, weight = edge.weight) )

                
        if isSpanAllVertices == False :
            edgechosen = min(cutEdges,key = lambda x: x.weight)
            minimumSpanningTree.add_edge(Edge(source = edgechosen.source, target = edgechosen.target, weight = edgechosen.weight))
            visited.append(edgechosen.target)
            notvisited.remove(edgechosen.target)

    print("The minimum Spanning Tree is : \n")

    minimumSpanningTree.edges
    #minimumSpanningTree.edges.sort(reverse = False, key = lambda x: x.source)

    for edge in minimumSpanningTree.edges:
        cost += edge.weight
        print(edge)

    print("\n" + "Minimum Cost Spanning Tree Cost:" + str(cost) + "\n")
    return

n=int(input("wprowadź ilość wierzchołków: "))
G = Graph(n, directed = False)

for i in range(1, n+1):
    G.add_node(i)

random_edges(G, n)

G.show()

primMST(G,1,n)
print ("BREAK")
print(MST(G,n))
