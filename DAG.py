import random, datetime, timeit, sys 
from random import randint
sys.setrecursionlimit(1500)

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
    
    def __invert__(self):                   #zwraca nową krawędź w przeciwnym kierunku
        return Edge(self.target, self.source, self.weight)

    inverted = __invert__


class Graph(dict):
    def __init__(self, n=0, directed = False):  #inicjalizuje obiekt grafu
        self.n = n
        self.directed = directed

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
        if edge.target not in self[edge.source]:
            self[edge.source][edge.target] = edge.weight
        else:
            raise ValueError("krawędzie równoległe sa zabronione(2)")
        if not self.is_directed():
            if edge.source not in self[edge.target]:
                self[edge.target][edge.source] = edge.weight
            else:
                raise ValueError("krawędzie równoległe sa zabronione(3)")

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


class Matrix_Graph (object):
    def __init__(self, n, directed=False):   #inicjalizuje obiekt grafu
        if n<0:
            raise ValueError("n musi byc liczba dodatnia")
        self.n=n
        self.directed = directed
        self.data=[[0]*self.n for node in range(self.n)]
        
    def is_directed(self):
        return self.directed
        
    def v(self):
        return self.n
    
    def e(self):
        counter=0
        for source in range(self.n):
            for target in range(self.n):
                if self.data[source][target] !=0:
                    counter=counter+1
        return (counter if self.directed else counter/2)

    def has_node(self, node):
        return 0<=node<self.n
        
    def add_edge(self, edge):
        if edge.source==edge.target:
            raise ValueError("petle sa zabronione")
        if self.data[edge.source][edge.target]==0:
            self.data[edge.source][edge.target]=edge.weight
        else:
            raise ValueError("krawedzie rownolegle sa zabronione")

    def del_edge(self, edge):
        self.data[edge.source][edge.target]=0
        if not self.directed:
            self.data[edge.target][edge.source]=0
            
    def has_edge(self, edge):
        return self.data[edge.source][edge.target] != 0
    
    def weight(self, edge):
        return self.data[edge.source][edge.target]
    
    def iternodes(self):
        return iter(range(self.n))
        
    def iteradjacent(self, source):
        for target in range(self.n):
            if self.data[source][target]!=0:
                yield target
            
    def iteroutedges(self, source):
        for target in range(self.n):
            if self.data[source][target]!=0:
                yield Edge(source, target, self.data[source][target])

    def iterinedges(self, source):
        for target in range(self.n):
            if self.data[target][source]!=0:
                yield Edge(target, source, self.data[target][source])

    def iteredges(self):
        for source in range(self.n):
            for target in (range(self.n)):
                if self.data[source][target]!=0 and (self.directed or source<target):
                    yield Edge(source, target, self.data[source][target])

    def show(self):
        for source in range(self.n):
            print(source+1, ":")
            for target in self.iteradjacent(source):
                print("%s(%s)" % (target+1, self.data[source][target]))

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
        graph.add_edge(Edge(j, k))
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
            graph.add_edge(Edge(i, new))
    
    return graph

class DFS():
    def __init__(self, graph):
        self.graph = graph
        self.previous = dict()

    def run(self, source=None, pre_action=None, post_action=None):    #metoda uruchamiająca dfs
        if source is not None:
            self.previous[source] = None    #przed wizytą
            self._visit(source, pre_action, post_action)
        else:
            for source in self.graph.iternodes():
                if source not in self.previous:
                    self.previous[source] = None
                    self._visit(source, pre_action, post_action)

    def _visit(self, source, pre_action, post_action):  #metoda odwiedzająca każdy V
        if pre_action:                      #akcja przy wejściu do source
            pre_action(source)
        for child in self.graph.iteradjacent(source):
            if child not in self.previous:
                self.previous[child] = source           #przed wizytą
                self._visit(child, pre_action, post_action)
        if post_action:
            post_action(source)             #akcja przy opuszczaniu source
       
class Topological_sort():
    def __init__(self, graph):
        self.graph = graph
        self.order = list()
        
    def run(self):
        DFS(self.graph).run(post_action = lambda node: self.order.append(node))
        self.order.reverse()

    def runM(self):                         #uruchamianie dla macierzy
        DFS(self.graph).run(post_action = lambda node: self.order.append(node+1))
        self.order.reverse()

file = open('czasy.txt', 'a')
file.write("LISTA\tMACIERZ\n")
#n=int(input("wprowadź ilość wierzchołków: "))

for x in range(3):
    for n in range(100, 1501, 100):
        print(n)
        G = Graph(n, directed = True)
        MG = Matrix_Graph(n, directed = True)

        for i in range(1, n+1):
            G.add_node(i)

        random_edges(G, n)
        for i in range(1, n+1):
            for j in range(i, n+1):
                if G.has_edge(Edge(i, j)):
                    MG.add_edge(Edge(i-1, j-1))

        top = Topological_sort(G)
        start = datetime.datetime.now()
        top.run()
        duration = datetime.datetime.now() - start
        DURATION=str(duration)
        score=DURATION[2:].replace('.', ',')
        file.write(score)
        file.write('\t')
        #print(top.order)

        topM = Topological_sort(MG)
        start = datetime.datetime.now()
        topM.runM()
        duration = datetime.datetime.now() - start
        DURATION=str(duration)
        score=DURATION[2:].replace('.', ',')
        file.write(score)
        file.write('\n')
        #print(topM.order)

        del G, MG
    file.write('\n')
file.close()
