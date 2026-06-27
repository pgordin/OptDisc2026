def five_color_planar(graph):
    if not graph:
        return {}

    # Jeśli graf ma 5 lub mniej wierzchołków,
    # każdy z nich dostaje po prostu inny kolor.
    if len(graph) <= 5:
        return {node: i + 1 for i, node in enumerate(graph.keys())}

    # Szukamy wierzchołka o najmniejszym stopniu w grafie
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    v = min(degrees, key=degrees.get)
    deg_v = degrees[v]

    # Sprawdzenie czy graf jest planarny
    if deg_v > 5:
        raise ValueError("Graf nie jest planarny.")

    # Tworzymy kopię grafu
    G_prime = {node: neighbors.copy() for node, neighbors in graph.items() if node != v}
    for neighbors in G_prime.values():
        neighbors.discard(v)

    # Przypadek 1 deg(v) < 5
    if deg_v < 5:
        # Po prostu kolorujemy kopię grafu
        colors = five_color_planar(G_prime)

        # Przywracamy v i nadajemy mu pierwszy wolny z 5 kolorów
        used_colors = {colors[neighbor] for neighbor in graph[v]}
        for color in range(1, 6):
            if color not in used_colors:
                colors[v] = color
                break

        return colors

    # Przypadek 2 deg(v) == 5
    else:
        # Szukamy dwóch sąsiadów x i y wierzchołka v, którzy nie są ze sobą połączeni
        neighbors_v = list(graph[v])
        x, y = None, None

        for i in range(len(neighbors_v)):
            for j in range(i + 1, len(neighbors_v)):
                if neighbors_v[j] not in graph[neighbors_v[i]]:
                    x, y = neighbors_v[i], neighbors_v[j]
                    break
            if x:
                break

        if not x:
            raise ValueError("Nie znaleziono x i y. Graf narusza zasady planarności.")

        # Dodajemy do x sąsiadów y
        for z in G_prime[y]:
            if z != x:
                G_prime[x].add(z)
                G_prime[z].add(x)
            # Usuwamy krawędzie prowadzące do y
            G_prime[z].discard(y)

        # Usuwamy całkowicie y z grafu
        del G_prime[y]

        colors = five_color_planar(G_prime)

        colors[y] = colors[x]

        used_colors = {colors[neighbor] for neighbor in graph[v]}
        for color in range(1, 6):
            if color not in used_colors:
                colors[v] = color
                break

        return colors


def solve_with_5_colors(raw_graph):
    graph_with_sets = {node: set(neighbors) for node, neighbors in raw_graph.items()}

    print(f"Liczba wierzchołków do pokolorowania: {len(raw_graph)}")
    result = five_color_planar(graph_with_sets)
    used_colors_count = max(result.values()) if result else 0

    print(f"Wynik 5-kolorowania: {result}")
    print(f"Użyte kolory: {used_colors_count}")

#Przykład

if __name__ == "__main__":
    test_graph = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C', 'E', 'F'],
        'C': ['A', 'B', 'D', 'E', 'G'],
        'D': ['A', 'C', 'F', 'G'],
        'E': ['B', 'C', 'F', 'H'],
        'F': ['B', 'D', 'E', 'H'],
        'G': ['C', 'D', 'H'],
        'H': ['E', 'F', 'G']
    }

    print("--- Start Konstruktywnego Algorytmu 5-Kolorowania ---")
    solve_with_5_colors(test_graph)