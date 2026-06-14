import heapq


def oblicz_heurystyke (punkt_a, punkt_b):
    """Oblicza odleglosc Manhattan miedzy dwoma punktami."""
    return abs(punkt_a[0] - punkt_b[0]) + abs(punkt_a[1] - punkt_b[1])


def a_star (mapa, start, meta):
    kolejka = []
    # Krotka w kolejce: (priorytet_f, pozycja)
    heapq.heappush(kolejka, (0, start))

    # Slowniki przechowujace historie krokow i najtanszy koszt
    skad_przyszlismy = {start: None}
    koszt_dojscia = {start: 0}

    while kolejka:
        # Pobieramy wezel o najnizszym koszcie f
        obecny_koszt_f, obecna_pozycja = heapq.heappop(kolejka)

        # Warunek koncowy - trafiono na mete
        if obecna_pozycja == meta:
            sciezka = []
            krok = meta
            while krok is not None:
                sciezka.append(krok)
                krok = skad_przyszlismy[krok]
            return sciezka[::-1]

            # Generowanie ruchow (prawo, lewo, dol, gora)
        ruchy = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for ruch in ruchy:
            sasiad = (obecna_pozycja[0] + ruch[0], obecna_pozycja[1] + ruch[1])

            # Sprawdzenie, czy nie wychodzimy poza mape
            if (sasiad[0] < 0 or sasiad[0] >= len(mapa) or
                    sasiad[1] < 0 or sasiad[1] >= len(mapa[0])):
                continue

            # Sprawdzenie kolizji ze sciana (wartosc != 0)
            if mapa[sasiad[0]][sasiad[1]] != 0:
                continue

            nowy_koszt = koszt_dojscia[obecna_pozycja] + 1

            # Aktualizacja, jesli znalezlismy krotsza droge do sasiada
            if sasiad not in koszt_dojscia or nowy_koszt < koszt_dojscia[sasiad]:
                koszt_dojscia[sasiad] = nowy_koszt
                priorytet_f = nowy_koszt + oblicz_heurystyke(sasiad, meta)

                heapq.heappush(kolejka, (priorytet_f, sasiad))
                skad_przyszlismy[sasiad] = obecna_pozycja

    return None


mapa_testowa = [
    [0, 0, 0, 0],
    [0, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 1, 0]
]
wynik = a_star(mapa_testowa, (0, 0), (3, 3))
print("Odnaleziona sciezka:", wynik)