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
            self.data[edge.target][edge.source]=edge.weight
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


    def printMST(self, parent): 
        print ("Edge \tWeight")
        for i in range(1,self.n): 
            print ((parent[i])+1,"-",i+1,"\t",(self.data[i][ parent[i]]))
  
    def minKey(self, key, mstSet): 
        mini = 9999
  
        for v in range(self.n): 
            if key[v] < mini and mstSet[v] == False: 
                mini = key[v] 
                min_index = v 
  
        return min_index 

    def primMST(self):  
        key = [9999] * self.n 
        parent = [None] * self.n
        key[0] = 0 
        mstSet = [False] * self.n 
  
        parent[0] = -1 
  
        for cout in range(self.n): 
            u = self.minKey(key, mstSet) 
            mstSet[u] = True
            for v in range(self.n): 
                if self.data[u][v] > 0 and mstSet[v] == False and key[v] > self.data[u][v]: 
                        key[v] = self.data[u][v] 
                        parent[v] = u 
  
        self.printMST(parent)

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

def MST(tab,n):
    TV=[1] #wierzcholki w drzewie -> 1 wierzcholek startowy
    T=[]  #krawedzie w drzewie -> na start lista pusta
    while len(T)<n-1:
        min =1001
        tmpu=n+1
        tmpv=n+1
        for u in TV:
            for v in range(n):
                if tab[u][v]>0 and tab[u][v]<min and ((v in TV)==False):
                    min=tab[u][v]
                    tmpu=u
                    tmpv=v
        if min==1001:
            break
        else:
            TV.append(tmpv)
            T.append([tmpu+1,tmpv+1])
    return T
            

n=int(input("wprowadź ilość wierzchołków: "))
G = Graph(n, directed = False)
MG = Matrix_Graph(n, directed = False)

for i in range(1, n+1):
    G.add_node(i)

random_edges(G, n)
for i in range(1, n+1):
    for j in range(i, n+1):
        #print(i, j)
        if G.has_edge(Edge(i, j)):
            weight = random.randint(1,1000)
            MG.add_edge(Edge(i-1, j-1,weight))

print("lista")
G.show()
print("macierz")
MG.show()
MG.primMST()

g = Matrix_Graph(5)
g.data = [ [0, 20, 0, 16, 0], 
            [20, 0, 3, 8, 5], 
            [0, 3, 0, 0, 7], 
            [16, 8, 0, 0, 9], 
            [0, 5, 7, 9, 0]]

print ("MACIERZ 2")
g.show()

g.primMST();

print ("BREAK")
print (MST(g.data,n))



