import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from random import random, seed
from copy import deepcopy

#funkcje grafowe z pierwszych zajęć
def print_matrix(vertices, matrix):
  """
  Wypisuje na ekranie graf podany jako macierz sąsiedztwa
  """
  n = len(matrix)
  if (vertices is None) or (len(vertices) != n):
    vv = range(1, n+1)
  else:
    vv = vertices
  for i in range(n):
    print(vv[i], ':', end='')
    for j in range(n):
      if (matrix[i][j]):
        print(" ", vv[j], end="")
    print("")


def print_dict(graph):
  """
  Wypisuje na ekranie graf podany jako słownik (list) sąsiedztwa
  """
  for v in graph:
    print(v, ':', end="")
    for u in graph[v]:
      print(" ", u, end="")
    print("")

#klasa Graph
class Graph:
    def __init__(self, graph=None, directed=0):
        if graph is None:
            graph = {}
        self.graph = graph
        self.directed = directed

    # inicjalizator ze słownika
    @classmethod
    def from_dict(cls, graph):
        return cls(graph)

    # inicjalizator z macierzy
    @classmethod
    def from_matrix(cls, matrix, vertices = None):
        if (vertices is None) or (len(vertices) != len(matrix)):
            vertices = [*range(1, len(matrix) + 1)]
        return cls.from_dict(cls._matrix_to_dict(matrix, vertices))

    # dwie prywatne metody macierz <-> słownik
    def _matrix_to_dict(matrix, vertices: list) -> dict:
        """
        Zamienia graf podany jako macierz sąsiedztwa na słownik sąsiedztwa.
        """
        res_dict = {}
        for i, v in enumerate(vertices):
            neighbours = [vertices[j] for j, edge in enumerate(matrix[i]) if edge]
            res_dict[v] = neighbours
        return res_dict

    def _dict_to_matrix(self, _dict: dict) -> np.array:
        """
        Zamienia graf podany jako słownik sąsiedztwa na macierz sąsiedztwa.
        """
        n = len(_dict)
        vertices = [*_dict.keys()]
        matrix = np.zeros(shape = (n, n), dtype=int)
        for u,v in [
            (vertices.index(u), vertices.index(v))
            for u, row in _dict.items() for v in row
        ]:
            matrix[u][v] += 1
        return matrix

    def vertices(self) -> list:
        """
        Zwraca listę wierzchołków grafu.
        """
        return [*self.graph.keys()]

    def matrix(self) -> np.array:
        """
        Zwraca macierz sąsiedztwa grafu.
        """
        return self._dict_to_matrix(self.graph)

    # przedefiniowania sposobu wyświetlania grafów
    def __str__(self):
        res = ""
        for v in self.graph:
            res += f"{v}:"
            for u in self.graph[v]:
                res += f" {u}"
            res += "\n"
        return res

    # Poniższe dostajemy za darmo z powyższego
    def to_neighbourlist(self, filename: str):
        """
        Zapisuje graf podany jako słownik (list) sąsiedztwa do pliku (w formie listy sąsiedztwa).
        Zmienna filename zawiera pełną ścieżkę pliku
        """
        file = open(filename, "w")  # otwarcie pliku tekstowego do zapisu
        file.write(str(self))
        file.close()

    # rysowanie grafów
    def plot(self, pos=None, directed=None):
      """
      Rysuje graf używając pakietu networkx
      """
      if directed is None:
        directed = self.directed
      if directed:
        G = nx.DiGraph(self.graph)
      else:
        G = nx.Graph(self.graph)

      if pos is None:
        pos = nx.spring_layout(G)
      nx.draw(G, pos, with_labels=True)
      plt.show()

    # Modyfikacje grafów
    def add_vertex(self, vertex):
        """
        Dodaje wierzchołek do grafu
        """
        if vertex not in self.graph:
            self.graph[vertex] = []

    def del_vertex(self, vertex):
        """
        Usuwa wierzchołek z grafu
        """
        if vertex in self.graph:
            self.graph.pop(vertex)
            for u in self.graph:
                if vertex in self.graph[u]:
                    self.graph[u].remove(vertex)

    def add_arc(self, arc):
        """
        Dodaje łuk (skierowany, podany jako para wierzchołków) do grafu
        """
        u, v = arc
        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self.graph[u]:
            self.graph[u].append(v)

    def add_edge(self, edge: list):
        """
        Dodaje krawędź (podaną jako para wierzchołków) do grafu
        Rozpatrujemy grafy proste, nieskierowane
        """
        u, v = edge
        if u == v:
            raise ValueError("Pętle nie są dopuszczalne!")
        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self.graph[u]:
            self.graph[u].append(v)
        if u not in self.graph[v]:
            self.graph[v].append(u)

    # czytanie z plików
    @staticmethod
    def from_edges(filename: str, directed = 0):
        """
        Tworzy graf na podstawie pliku z łukami/krawędziami.
        Opis łuku/krawędzi to dwa słowa lub wierzchołka (jedno słowo).
        Nadmiarowe słowa są ignorowane.
        Zmienna filename zawiera pełną ścieżkę pliku
        """
        graph = Graph(directed=directed)
        file = open(filename, "r")          # otwarcie pliku do odczytu
        for line in file:                   # dla każdej linii w pliku
          words = line.strip().split()      # rozdziel linię na słowa
          if len(words) == 1:               # jedno słowo - opis wierzchołka
            graph.add_vertex(words[0])
          elif len(words) >= 2:             # conajmnej 2 słowa - opis krawędzi/łuku
            if directed:
              graph.add_arc([words[0], words[1]])
            else:
              graph.add_edge([words[0], words[1]])
        file.close()
        return graph

    # zapisywanie grafu do pliku w postaci listy krawędzi,
    def graph_to_edges(self, filename):
      with open(filename, 'w') as file:
        visited = set() # żeby się nie powtarzały krawędzie
        for v in self.graph:
          for u in self.graph[v]:
            if self.directed:
              file.write(f"{v} {u}\n") # każda krawędź w osobnym wierszu
            else:
              if (u, v) not in visited:
                file.write(f"{v} {u}\n")
                visited.add((v, u))

    @staticmethod
    def from_neighbourlist(filename, directed=0):
      """
      wczytywanie grafu z listy sąsiedztwa
      """
      graph = Graph(directed=directed)
      with open(filename, 'r') as file:
        for line in file:
          parts = line.strip().split(":")

          v = parts[0].strip()
          graph.add_vertex(v)

          if len(parts) > 1:
            neighbours = parts[1].strip().split()

            for u in neighbours:
              if directed:
                graph.add_arc((v,u))
              else:
                graph.add_edge((v,u))
      return graph

    @staticmethod
    def random_graph(n: int, p: float):
        """
        Tworzy losowy graf nieskierowany G(n,p)
        """
        rand_graph = Graph()
        for i in range(1, n + 1):
            rand_graph.add_vertex(i)
            for j in range(1, i):
                if random() < p:
                    rand_graph.add_edge([i, j])
        return rand_graph

    @staticmethod
    def cycle(n: int):
        """
        Tworzy graf cykliczny o n wierzchołkach
        """
        cycle = Graph()
        for i in range(n-1):
          cycle.add_edge([i+1, i+2])
        cycle.add_edge([1, n])
        return cycle


    def Prufer(self):
        """
        Zwraca kod Prüfera dla drzewa.
        Uwaga: nie jest sprawdzane, czy graf jest drzewem!!!
        kod będzie zrócony jako napis.
        """
        tr = deepcopy(self.graph)     # kopia słownika, bo go zepsuję
        code = ""
        for i in range(len(self.graph)-2):
          for x in sorted(tr):
            if len(tr[x]) == 1:     # najmniejszy liść
              break
          v = tr[x][0]    # sąsiad x
          code += f"{v} "
          tr.pop(x)
          tr[v].remove(x)
        return code.strip()


    def tree_from_Prufer(code : str):
        """
        Tworzy drzewo na podstawie kodu Prüfera.
        """
        tree = Graph()
        clist = [int(x) for x in code.strip().split()]  # kod jako lista
        n = len(clist) + 2
        vert = [x for x in range(1, n+1)]
        for v in vert:
          tree.add_vertex(v)
        for i in range(n-2):
          for x in vert:
            if x not in clist:  # najmniejszy liśc
              break
          v = clist.pop(0)    # sąsiad x
          tree.add_edge((x, v))
          vert.remove(x)
        tree.add_edge(vert)   # ostatnie 2 wierzchołki tworzą krawędź
        return tree


    def connected_components(self):
      """
      Zwraca listę składowych spójnych grafu, jako listę zbiorów wierzchołków.
      Uwaga: zerowy element listy zawiera wszystkie wierzchołki grafu.
      """
      def DFS(u):
        """
        Przechodzenie w głąb - funkcja wewnętrzna
        """
        for w in self.graph[u]:
          if w not in VT[0]:
            VT[0].add(w)
            VT[-1].add(w)
            DFS(w)
      """
      VT - lista zbiorów wierzchołków
      VT[0] - docelowo zbiór wszystkich wierzchołków grafu
      """
      VT = [set([])]
      for v in self.graph:
        if v not in VT[0]:    # jeżeli v nieodwiedzony
          VT[0].add(v)        # v - już odwiedzony
          VT.append(set([v])) # zalążek nowej spójnej składowej
          DFS(v)
      return VT


    def connected_components_graphs(self):
      """
      Zwraca listę spójnych składowych (nieskierowanego) grafu jako listę grafów.
      """
      components = self.connected_components()
      graphs = []
      for comp in components[1:]:
        subgraph = Graph()
        for v in comp:
          subgraph.graph[v] = self.graph[v].copy()
        graphs.append(subgraph)
      return graphs


    def distance(self, v):
      """
      Zwraca słownik odległości wierzchołka v do innych osiągalnych wierzchołków.
      Używa BFS
      """
      dist = {v:0}    # zalążek słownika
      queue = [v]     # kolejka wierzchołków
      while queue:
        u = queue.pop(0)
        for w in self.graph[u]:
          if w not in dist:
            dist[w] = dist[u] + 1
            queue.append(w)
      return dist


    def preorder(self, v, visited=None):
      """
       Wypisuje drzewo w porządku preorder, zaczynając od wierzchołka v.
        Uwaga: nie jest sprawdzane, czy graf jest drzewem, ale w tej wersji się nie zawiesi.
      """
      if visited is None:
        visited = set()

      visited.add(v)
      print(v, end=" ")

      for u in self.graph[v]:
        if u not in visited:
          self.preorder(u, visited)


    def postorder(self, v, visited=None):
       """
        Wypisuje drzewo w porządku postorder, zaczynając od wierzchołka v.
        Uwaga: nie jest sprawdzane, czy graf jest drzewem, ale w tej wersji się nie zawiesi.
       """
       if visited is None:
          visited = set()

       visited.add(v)

       for u in self.graph[v]:
          if u not in visited:
            self.postorder(u, visited)

       print(v, end=" ")

    @staticmethod
    def random_bipartite_graph(n: int, p: float):
        """
        Tworzy losowy graf dwudzielny o 2n wierzchołkach.
        Pierwsza część to wierzchołki 1, 2, ..., n,
        druga część to wierzchołki n+1, n+2, ..., 2n.
        Każda możliwa krawędź między częściami jest losowana
        niezależnie z prawdopodobieństwem p.
        """
        #pusty graf
        g = Graph()

        # podział na dwie części
        A = list(range(1, n + 1))
        B = list(range(n + 1, 2*n + 1))

        # wierzchołki
        for v in A + B:
          g.add_vertex(v)

        # losowe krawędzie
        for u in A:
          for v in B:
            if random() < p:
                g.add_edge([u, v])

        return g

#Klasa WeightedGraph
from queue import PriorityQueue

class WeightedGraph(Graph):
    def __init__(self, graph=None, directed=0, weights=None):
        super().__init__(graph, directed)
        if weights is None:
            weights = {}
        self.weights = weights

    @classmethod
    def from_dict(cls, graph, weights):
        return cls(graph, weights=weights)

    # przedefiniowanie sposobu wyświetlania grafów
    def __str__(self):
        res = ""
        for v in self.graph:
            res += f"{v}:"
            for u in self.graph[v]:
                res += f" {u}({self.weights[(v, u)]})"
            res += "\n"
        return res

    # rysowanie grafów
    def plot(self, pos=None, directed=None):
      """
      Rysuje graf używając pakietu networkx
      """
      if directed is None:
        directed = self.directed
      if directed:
        G = nx.DiGraph(self.graph)
      else:
        G = nx.Graph(self.graph)

      if pos is None:
        pos = nx.spring_layout(G)
      nx.draw(G, pos, with_labels=True)
      labels = self.weights
      nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.3)

      plt.show()

    def add_arc(self, arc, weight = 1):
        """
        Dodaje łuk (skierowany, podany jako para wierzchołków) do grafu
        """
        super().add_arc(arc)
        self.weights[arc] = weight

    def add_edge(self, edge: list, weight = 1):
        """
        Dodaje krawędź (podaną jako para wierzchołków) do grafu
        Rozpatrujemy grafy proste, nieskierowane
        """
        u, v = edge
        super().add_edge(edge)
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight

    def del_arc(self, arc):
        """
        Usuwa łuk (skierowany, podany jako para wierzchołków) z grafu
        """
        super().del_arc(arc)
        self.weights.pop(arc)


    # czytanie z plików
    @staticmethod
    def from_edges(filename: str, directed = 0):
        """
        Tworzy graf na podstawie pliku z łukami/krawędziami.
        Opis łuku/krawędzi to dwa słowa lub wierzchołka (jedno słowo),
        lub 3 słowa dla ważonych łuków/krawędzi.
        Nadmiarowe słowa są ignorowane.
        Zmienna filename zawiera pełną ścieżkę pliku
        """
        wgraph = WeightedGraph(directed=directed)
        file = open(filename, "r")          # otwarcie pliku do odczytu
        for line in file:                   # dla każdej linii w pliku
          words = line.strip().split()      # rozdziel linię na słowa
          if len(words) == 1:               # jedno słowo - opis wierzchołka
            wgraph.add_vertex(words[0])
          elif len(words) == 2:             # 2 słowa - opis krawędzi/łuku z domyślną wagą
            if directed:
              wgraph.add_arc([words[0], words[1]])
            else:
              wgraph.add_edge([words[0], words[1]])
          elif len(words) >= 3:             # co najmniej 3 słowa - ważony łuk/krawędź
            if directed:
              wgraph.add_arc([words[0], words[1]], int(words[2]))
            else:
              wgraph.add_edge([words[0], words[1]], int(words[2]))
        file.close()
        return wgraph


    def min_spanning_tree(self):
        """
        Zwraca drzewo rozpinające grafu ważonego. Algorytm Jarnika-Prima
        """
        wtree = WeightedGraph()
        for v in self.graph:
          wtree.add_vertex(v)
          break
        total = 0   # łączna waga krawędzo drzewa
        q = PriorityQueue()
        for u in self.graph[v]:
          q.put((self.weights[(v, u)], v, u))
        while not q.empty():
          w, v, u = q.get()
          if u not in wtree.graph:
            wtree.add_edge([u, v], w)
            total += w
            for x in self.graph[u]:
              if x not in wtree.graph:
                q.put((self.weights[(u, x)], u, x))

        if len(wtree.graph) != len(self.graph):
          print("Graf niespojny! Zwrócone drzewo spinające jedną składową.")
        return wtree, total

    #------------------------Zadanie 5--------------------------------
    def vertices(self):
        """
        Zwraca listę wierzchołków grafu (klucze słownika self.graph)
        """
        return list(self.graph.keys())


    def matrix(self, no_edge=float('inf')):
        """
        Zamienia graf ważony (listę i wagi) na macierz wag
        """
        vertices = self.vertices()
        #każdemu wierzcholkowi przypisujemy indeks w macierzy
        index = {v: i for i, v in enumerate(vertices)}
        n = len(vertices)

        #tworzymy macierz nxn (wypełniona brakiem krawędzi)
        mat = [[no_edge for _ in range(n)] for _ in range(n)]

        #odleglosc wierzcholka do samego siebie = 0
        for i in range(n):
            mat[i][i] = 0

        # wpisywanie wag
        for (u, v), w in self.weights.items():
            if u in index and v in index:
                mat[index[u]][index[v]] = w

        return vertices, mat  #zwracamy kolejnosc wierzcholkow oraz macierz wag


    @classmethod
    def from_matrix(cls, matrix, vertices=None, directed=0, no_edge=float('inf')):
        """
        Zamienia macierz wag na graf ważony
        """

        n = len(matrix)

        # jeśli nie podano nazw wierzchołków
        if vertices is None:
            vertices = list(range(1, n + 1))

        #tworzymy pusty graf
        graph = cls(directed=directed)

        # dodaj wierzchołki
        for v in vertices:
            graph.add_vertex(v)

        # przejście po macierzy
        for i in range(n):
            for j in range(n):

                w = matrix[i][j]

                # pomijamy brak krawędzi i przekątną
                if i != j and w != no_edge:
                    u = vertices[i]
                    v = vertices[j]

                    if directed:
                        graph.add_arc([u, v], w)
                    else:
                        # żeby nie dublować krawędzi w grafie nieskierowanym
                        if i < j:
                            graph.add_edge([u, v], w)

        return graph





    def floyd_warshall(self, no_edge=float('inf')):
        """
        Algorytm Floyda-Warshalla:
        zwraca macierz najkrótszych odległości między każdą parą wierzchołków
        """
        #zamienmy graf na macierz wag
        vertices, dist = self.matrix(no_edge=no_edge)
        n = len(dist)

        #dla każdej trasy o początku w wierzchołku i, końcu w wierzchołku j,
        #sprawdzamy, czy opłaca się przejść między nimi pośrednio przez k
        for k in range(n):
            for i in range(n):
                for j in range(n):

                    # sprawdzamy czy przejscie przez k daje krótszą drogę
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return vertices, dist #zwracamy listę wierzcholkow oraz macierz najkrotszych odleglosci

#testowanie
g = WeightedGraph(directed=0)

g.add_edge(["A", "B"], 3)
g.add_edge(["A", "C"], 5)
g.add_edge(["B", "C"], 2)

vertices, mat = g.matrix()

print("Wierzchołki:", vertices)
print("Macierz:")
for row in mat:
    print(row)

vertices = ["A", "B", "C"]

matrix = [
    [0, 3, 5],
    [3, 0, 2],
    [5, 2, 0]
]

g2 = WeightedGraph.from_matrix(matrix, vertices, directed=0)

print(g2)

#macierz odleglosci
g = WeightedGraph()

g.add_edge(["A", "B"], 3)
g.add_edge(["B", "C"], 2)
g.add_edge(["A", "C"], 10)

vertices, dist = g.floyd_warshall()

print(vertices)
for row in dist:
    print(row)