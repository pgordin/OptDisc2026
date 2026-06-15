def is_safe(vertex, color, graph, current_coloring):
    """
    Sprawdza, czy można bezpiecznie przypisać 'color' do 'vertex'.
    Weryfikuje, czy żaden z sąsiadów nie ma już tego samego koloru.
    """
    for neighbor in graph[vertex]:
        if neighbor in current_coloring and current_coloring[neighbor] == color:
            return False
    return True


def graph_coloring_backtracking(graph, vertices, current_index, current_coloring, palette):
    """
    Rekurencyjny algorytm z nawrotami (backtracking) do kolorowania mapy.
    """
    # Jeśli przeszliśmy przez wszystkie wierzchołki, sukces!
    if current_index == len(vertices):
        return True

    vertex = vertices[current_index]

    # Próbujemy przypisać każdy z 5 kolorów z palety
    for color in palette:
        if is_safe(vertex, color, graph, current_coloring):
            # Przypisujemy kolor
            current_coloring[vertex] = color

            # Rekurencyjnie idziemy do następnego wierzchołka
            if graph_coloring_backtracking(graph, vertices, current_index + 1, current_coloring, palette):
                return True

            # Jeśli ścieżka nie dała rozwiązania, cofamy wybór (backtrack)
            del current_coloring[vertex]

    # Jeśli żaden kolor nie pasuje, zwracamy False
    return False


def solve_5_coloring(graph, name):
    """
    Funkcja pomocnicza przygotowująca dane i uruchamiająca algorytm dla maksymalnie 5 kolorów.
    """
    palette = ["Czerwony", "Zielony", "Niebieski", "Żółty", "Fioletowy"]
    vertices = list(graph.keys())
    current_coloring = {}

    print(f"--- Kolorowanie mapy: {name} ---")

    if graph_coloring_backtracking(graph, vertices, 0, current_coloring, palette):
        # Policz, ilu z 5 dostępnych kolorów faktycznie użyto
        used_colors = set(current_coloring.values())
        print(f"Sukces! Wynik: {current_coloring}")
        print(f"Faktycznie użyto {len(used_colors)} kolorów z dostępnych 5: {used_colors}\n")
    else:
        # Dla grafów planarnych ten warunek nigdy nie powinien się spełnić
        print("Nie udało się pokolorować grafu za pomocą 5 kolorów.\n")


# PRZYKŁADY Z RÓŻNYCH KLAS GRAFÓW PLANARNYCH

if __name__ == "__main__":
    # 1. Drzewo (Linia/Prosta mapa) - wymaga tylko 2 kolorów
    tree_graph = {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['B', 'D'],
        'D': ['C']
    }

    # 2. Cykl Nieparzysty (Pierścień 5 regionów) - wymaga 3 kolorów
    odd_cycle_graph = {
        '1': ['2', '5'],
        '2': ['1', '3'],
        '3': ['2', '4'],
        '4': ['3', '5'],
        '5': ['4', '1']
    }

    # 3. Graf K_4 (np. cztery kraje, gdzie każdy graniczy z każdym) - wymaga dokładnie 4 kolorów
    k4_graph = {
        'Region_W': ['Region_X', 'Region_Y', 'Region_Z'],
        'Region_X': ['Region_W', 'Region_Y', 'Region_Z'],
        'Region_Y': ['Region_W', 'Region_X', 'Region_Z'],
        'Region_Z': ['Region_W', 'Region_X', 'Region_Y']
    }

    # 4. Złożona Mapa (Uproszczony wycinek województw)
    # Centralne otoczone innymi
    poland_map = {
        'Mazowieckie': ['Kujawsko-Pomorskie', 'Warmińsko-Mazurskie', 'Podlaskie', 'Lubelskie', 'Świętokrzyskie',
                        'Łódzkie'],
        'Łódzkie': ['Mazowieckie', 'Świętokrzyskie', 'Śląskie', 'Opolskie', 'Wielkopolskie', 'Kujawsko-Pomorskie'],
        'Kujawsko-Pomorskie': ['Mazowieckie', 'Łódzkie', 'Wielkopolskie', 'Pomorskie', 'Warmińsko-Mazurskie'],
        'Wielkopolskie': ['Łódzkie', 'Kujawsko-Pomorskie', 'Zachodniopomorskie', 'Lubuskie', 'Dolnośląskie',
                          'Opolskie'],
        # Zewnętrzne granice (tylko z powyższymi w ramach tego małego wycinka)
        'Warmińsko-Mazurskie': ['Kujawsko-Pomorskie', 'Mazowieckie', 'Podlaskie'],
        'Podlaskie': ['Warmińsko-Mazurskie', 'Mazowieckie', 'Lubelskie'],
        'Lubelskie': ['Podlaskie', 'Mazowieckie', 'Świętokrzyskie'],
        'Świętokrzyskie': ['Lubelskie', 'Mazowieckie', 'Łódzkie', 'Śląskie', 'Małopolskie'],
        'Śląskie': ['Świętokrzyskie', 'Łódzkie', 'Opolskie', 'Małopolskie'],
        'Opolskie': ['Śląskie', 'Łódzkie', 'Wielkopolskie', 'Dolnośląskie'],
        'Dolnośląskie': ['Opolskie', 'Wielkopolskie', 'Lubuskie'],
        'Lubuskie': ['Dolnośląskie', 'Wielkopolskie', 'Zachodniopomorskie'],
        'Zachodniopomorskie': ['Lubuskie', 'Wielkopolskie', 'Pomorskie'],
        'Pomorskie': ['Zachodniopomorskie', 'Kujawsko-Pomorskie', 'Warmińsko-Mazurskie'],
        'Małopolskie': ['Śląskie', 'Świętokrzyskie']
    }

    # Uruchomienie testów
    solve_5_coloring(tree_graph, "Drzewo (Prosta granica)")
    solve_5_coloring(odd_cycle_graph, "Cykl nieparzysty (Pierścień)")
    solve_5_coloring(k4_graph, "Graf K4 (Maksymalny planarny dla 4 wierzchołków)")
    solve_5_coloring(poland_map, "Złożona Mapa (Fragment Polski)")