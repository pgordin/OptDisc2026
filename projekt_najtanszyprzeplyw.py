import collections

# Najtańszy przepływ o zadanej wielkości/maksymalny

# Klasa krawedz - Opisuje pojedynczą drogę między dwoma punktami
class Krawedz:
    def __init__(self, u, v, pojemnosc, koszt):
        self.u = u                # Wierzchołek startowy (skąd wyjeżdżamy)
        self.v = v                # Wierzchołek końcowy (dokąd jedziemy)
        self.pojemnosc = pojemnosc  # Maksymalny limit przesyłu (np. 10 ciężarówek)
        self.koszt = koszt        # Koszt przesłania jednej jednostki tą drogą
        self.przeplyw = 0         # Ile jednostek AKTUALNIE tędy płynie (na start 0)
        
        # Referencja do krawędzi powrotnej (szczątkowej). 
        # Robimy to, aby móc w przyszłości wycofywać błędne decyzje algorytmu.
        self.odwrotna = None      


# klasa SiecPrzepływowa - Zarządza całym grafem i logiką algorytmu
class SiecPrzepływowa:
    def __init__(self, liczba_wierzcholkow):
        self.n = liczba_wierzcholkow
        # Tworzymy listę sąsiedztwa. Dla każdego wierzchołka trzymamy listę wychodzących z niego dróg.
        self.graf = [[] for _ in range(liczba_wierzcholkow)]
        
    def dodaj_krawedz(self, u, v, pojemnosc, koszt):
        """
        Dodaje drogę do grafu. Zawsze dodaje dwie krawędzie: 
        1. Rzeczywistą (wprost)
        2. Wirtualną (powrotną) o ujemnym koszcie i początkowej pojemności 0.
        """
        wprost = Krawedz(u, v, pojemnosc, koszt)
        powrotna = Krawedz(v, u, 0, -koszt) # Ujemny koszt pozwala "odzyskać" pieniądze przy cofaniu
        
        # Łączymy krawędzie ze sobą, by wiedziały o swoim istnieniu
        wprost.odwrotna = powrotna
        powrotna.odwrotna = wprost
        
        # Dodajemy krawędzie do grafu
        self.graf[u].append(wprost)
        self.graf[v].append(powrotna)

    def _znajdz_najtansza_sciezke(self, zrodlo, ujscie):
        """
        Algorytm SPFA (Shortest Path Faster Algorithm). 
        Szuka najtańszej (niekoniecznie najkrótszej w sensie liczby krawędzi) 
        trasy ze źródła do ujścia.
        """
        # Inicjalizacja tablic pomocniczych
        odleglosci = [float('inf')] * self.n  # Na start wszędzie jest "nieskończenie" drogo
        rodzic = [None] * self.n              # Zapamiętujemy, którą krawędzią dotarliśmy do węzła (do odtworzenia trasy)
        w_kolejce = [False] * self.n          # Flagi zapobiegające wielokrotnemu dodawaniu tego samego węzła do kolejki
        
        odleglosci[zrodlo] = 0
        kolejka = collections.deque([zrodlo])
        w_kolejce[zrodlo] = True
        
        # Przeszukiwanie grafu
        while kolejka:
            u = kolejka.popleft() # Pobieramy węzeł do analizy
            w_kolejce[u] = False
            
            for krawedz in self.graf[u]:
                # Sprawdzamy, czy na tej krawędzi jest jeszcze w ogóle wolne miejsce
                wolna_pojemnosc = krawedz.pojemnosc - krawedz.przeplyw
                
                # Jeśli jest miejsce ORAZ dotarcie do sąsiada tą krawędzią jest tańsze niż znane dotychczas sposoby:
                if wolna_pojemnosc > 0 and odleglosci[krawedz.v] > odleglosci[u] + krawedz.koszt:
                    odleglosci[krawedz.v] = odleglosci[u] + krawedz.koszt # Aktualizujemy koszt
                    rodzic[krawedz.v] = krawedz                           # Zapisujemy "ślad"
                    
                    # Dodajemy sąsiada do kolejki (jeśli go tam nie ma), bo jego nowy koszt może poprawić koszty jego sąsiadów
                    if not w_kolejce[krawedz.v]:
                        kolejka.append(krawedz.v)
                        w_kolejce[krawedz.v] = True
                        
        # Zwracamy dwie rzeczy: 
        # 1. True/False - czy udało się dotrzeć do ujścia?
        # 2. rodzic - tablica pozwalająca odtworzyć drogę od końca do początku
        return odleglosci[ujscie] != float('inf'), rodzic

    def oblicz_najtanszy_przeplyw(self, zrodlo, ujscie, zadany_przeplyw=None):
        """
        Główna pętla algorytmu. Szuka kolejnych najtańszych ścieżek i "wpycha" 
        w nie przepływ, dopóki nie osiągnie celu (zadany_przeplyw) lub do momentu, 
        gdy graf się zapcha (maksymalny przepływ).
        """
        calkowity_przeplyw = 0
        calkowity_koszt = 0
        
        while True:
            # 1. WARUNEK STOPU DLA PRZEPŁYWU O ZADANEJ WIELKOŚCI
            # Jeśli mieliśmy przesłać konkretną ilość i już to zrobiliśmy - kończymy.
            if zadany_przeplyw is not None and calkowity_przeplyw >= zadany_przeplyw:
                break
                
            # 2. SZUKANIE TRASY
            istnieje_sciezka, rodzic = self._znajdz_najtansza_sciezke(zrodlo, ujscie)
            
            # WARUNEK STOPU DLA PRZEPŁYWU MAKSYMALNEGO
            # Jeśli zwiadowca nie znalazł ścieżki, sieć jest zapchana na maksa - kończymy.
            if not istnieje_sciezka:
                break 
                
            # 3. SZUKANIE "WĄSKIEGO GARDŁA" NA ZNALEZIONEJ TRASIE
            pchnij = float('inf')
            
            # Jeśli mamy limit, nie chcemy pchnąć więcej, niż brakuje do celu
            if zadany_przeplyw is not None:
                pchnij = min(pchnij, zadany_przeplyw - calkowity_przeplyw)
                
            # Cofamy się od ujścia do źródła po śladach z tablicy `rodzic`
            curr = ujscie
            while curr != zrodlo:
                kr = rodzic[curr]
                # Szukamy krawędzi o najmniejszej wolnej pojemności na tej trasie
                pchnij = min(pchnij, kr.pojemnosc - kr.przeplyw)
                curr = kr.u
                
            # Bezpiecznik: jeśli nie da się nic pchnąć, przerywamy (nie powinno się zdarzyć)
            if pchnij <= 0:
                break
                
            # 4. FIZYCZNE WPROWADZENIE PRZEPŁYWU W SIEĆ (AKTUALIZACJA)
            # Znowu cofamy się po śladach od ujścia do źródła i dodajemy/odejmujemy wartości
            curr = ujscie
            while curr != zrodlo:
                kr = rodzic[curr]
                kr.przeplyw += pchnij             # Zwiększamy obciążenie na krawędzi wprost
                kr.odwrotna.przeplyw -= pchnij    # ZMNIEJSZAMY na powrotnej (odblokowując możliwość cofania decyzji)
                calkowity_koszt += pchnij * kr.koszt # Dodajemy koszty transportu
                curr = kr.u
                
            # Aktualizujemy główny licznik przesłanego towaru
            calkowity_przeplyw += pchnij
            
        return calkowity_przeplyw, calkowity_koszt



# Przykłady

if __name__ == "__main__":
    
    # PARAMETRY GLOBALNE
    zrodlo = 0
    ujscie = 3
    
    print("NAJTAŃSZY PRZEPŁYW O ZADANEJ WIELKOŚCI")
    
    # Tworzymy pierwszą sieć z 4 wierzchołkami (0, 1, 2, 3)
    siec_zadana = SiecPrzepływowa(4)
    # Parametry: dodaj_krawedz(skad, dokad, limit_pojemnosci, koszt_jednostkowy)
    siec_zadana.dodaj_krawedz(0, 1, 10, 2)
    siec_zadana.dodaj_krawedz(0, 2, 5, 5)
    siec_zadana.dodaj_krawedz(1, 2, 4, 1)
    siec_zadana.dodaj_krawedz(1, 3, 7, 6)
    siec_zadana.dodaj_krawedz(2, 3, 10, 2)
    
    V = 8 # Chcemy przesłać dokładnie 8 jednostek
    f_ilosc, f_koszt = siec_zadana.oblicz_najtanszy_przeplyw(zrodlo, ujscie, zadany_przeplyw=V)
    
    print(f"Cel: Przesłać {V} jednostek.")
    print(f"Wynik -> Przesłano: {f_ilosc} | Całkowity koszt: {f_koszt} zł\n")

    print("NAJTAŃSZY PRZEPŁYW MAKSYMALNY")
    
    # Tworzymy sieć na nowo (żeby drogi nie były zapchane z poprzedniego zadania)
    siec_max = SiecPrzepływowa(4)
    siec_max.dodaj_krawedz(0, 1, 10, 2)
    siec_max.dodaj_krawedz(0, 2, 5, 5)
    siec_max.dodaj_krawedz(1, 2, 4, 1)
    siec_max.dodaj_krawedz(1, 3, 7, 6)
    siec_max.dodaj_krawedz(2, 3, 10, 2)
    
    # Wywołujemy funkcję BEZ podawania targetu. Algorytm zatrzyma się, gdy sieć będzie pełna.
    max_ilosc, max_koszt = siec_max.oblicz_najtanszy_przeplyw(zrodlo, ujscie)
    
    print("Cel: Przesłać absolutne maksimum możliwe dla tej sieci rur/dróg.")
    
    print(f"Wynik -> Przesłano: {max_ilosc} | Najmniejszy możliwy koszt obsłużenia maksimum: {max_koszt} zł")
  
    # BARDZIEJ ZŁOŻONY PRZYKŁAD (10 węzłów: od 0 do 9)

    print("BARDZIEJ ZŁOŻONA SIEĆ (10 WĘZŁÓW)")
    
    # Tworzymy sieć dla 10 węzłów
    siec_zlozona = SiecPrzepływowa(10)
    
    zrodlo_zlozone = 0
    ujscie_zlozone = 9
    
    # Budujemy sieć warstwowo. Węzły 1-8 to miasta pośrednie.
    # Parametry: dodaj_krawedz(skad, dokad, limit_pojemnosci, koszt_jednostkowy)
    
    # Warstwa 1 (krawędzie wychodzące ze źródła)
    siec_zlozona.dodaj_krawedz(0, 1, 15, 2)
    siec_zlozona.dodaj_krawedz(0, 2, 10, 4)
    siec_zlozona.dodaj_krawedz(0, 3, 12, 3)
    
    # Warstwa 2 (środek sieci)
    siec_zlozona.dodaj_krawedz(1, 4, 10, 1)
    siec_zlozona.dodaj_krawedz(1, 5, 5,  6)
    siec_zlozona.dodaj_krawedz(2, 5, 8,  2)
    siec_zlozona.dodaj_krawedz(2, 6, 7,  5)
    siec_zlozona.dodaj_krawedz(3, 6, 15, 1)
    
    # Warstwa 3 (środek sieci)
    siec_zlozona.dodaj_krawedz(4, 7, 12, 4)
    siec_zlozona.dodaj_krawedz(5, 7, 6,  3)
    siec_zlozona.dodaj_krawedz(5, 8, 9,  2)
    siec_zlozona.dodaj_krawedz(6, 8, 14, 3)
    
    # Warstwa 4 (krawędzie wchodzące do ujścia)
    siec_zlozona.dodaj_krawedz(7, 9, 15, 2)
    siec_zlozona.dodaj_krawedz(8, 9, 20, 3)
    
    # Dodatkowe krawędzie / "skróty" (np. droższe, ale dające dodatkową przepustowość)
    siec_zlozona.dodaj_krawedz(1, 8, 4, 10)
    siec_zlozona.dodaj_krawedz(4, 9, 5, 15)
    
    # Przepływ o zadanej wielkości
    V_zlozone = 20
    ilosc_zlozona, koszt_zlozony = siec_zlozona.oblicz_najtanszy_przeplyw(zrodlo_zlozone, ujscie_zlozone, zadany_przeplyw=V_zlozone)
    print(f"Cel: Przesłać dokładnie {V_zlozone} jednostek w złożonej sieci.")
    print(f"Wynik -> Przesłano: {ilosc_zlozona} | Całkowity koszt: {koszt_zlozony} zł\n")
    
    # Przepływ maksymalny w złożonej sieci
    # Ponieważ poprzedni test "zużył" część pojemności na drogach, 
    # tworzymy identyczną sieć na nowo dla czystego wyniku przepływu maksymalnego.
    siec_zlozona_max = SiecPrzepływowa(10)
    
    # Szybkie skopiowanie tych samych krawędzi
    dane_krawedzi = [
        (0, 1, 15, 2), (0, 2, 10, 4), (0, 3, 12, 3),
        (1, 4, 10, 1), (1, 5, 5, 6),  (2, 5, 8, 2), (2, 6, 7, 5), (3, 6, 15, 1),
        (4, 7, 12, 4), (5, 7, 6, 3),  (5, 8, 9, 2), (6, 8, 14, 3),
        (7, 9, 15, 2), (8, 9, 20, 3),
        (1, 8, 4, 10), (4, 9, 5, 15)
    ]
    for u, v, poj, ksz in dane_krawedzi:
        siec_zlozona_max.dodaj_krawedz(u, v, poj, ksz)
    
    # Uruchamiamy bez podawania limitu `zadany_przeplyw`
    max_ilosc_zl, max_koszt_zl = siec_zlozona_max.oblicz_najtanszy_przeplyw(zrodlo_zlozone, ujscie_zlozone)
    print("Cel: Przesłać absolutne maksimum możliwe dla złożonej sieci (10 węzłów).")
    print(f"Wynik -> Przesłano maksymalnie: {max_ilosc_zl} | Najmniejszy możliwy koszt: {max_koszt_zl} zł")

