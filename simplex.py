import numpy as np


class SimplexSolver:

    def __init__(self):
        self.tableau = None
        self.num_variables = 0
        self.num_constraints = 0

    def create_problem(self):

        print("=" * 60)
        print("PROGRAM ROZWIAZUJACY ZADANIA PROGRAMOWANIA LINIOWEGO")
        print("METODA SIMPLEX")
        print("=" * 60)

        self.num_variables = int(input("Liczba zmiennych decyzyjnych: "))
        self.num_constraints = int(input("Liczba ograniczen: "))

        print("\nPodaj wspolczynniki funkcji celu")
        objective = []

        for i in range(self.num_variables):
            value = float(input(f"x{i+1}: "))
            objective.append(value)

        constraints = []
        rhs = []

        print("\nPodaj ograniczenia w postaci <= ")

        for i in range(self.num_constraints):

            print(f"\nOgraniczenie {i+1}")

            row = []

            for j in range(self.num_variables):
                value = float(input(f"Wspolczynnik przy x{j+1}: "))
                row.append(value)

            b = float(input("Prawa strona: "))

            constraints.append(row)
            rhs.append(b)

        self.build_tableau(objective, constraints, rhs)

    def build_tableau(self, objective, constraints, rhs):

        rows = self.num_constraints + 1
        cols = self.num_variables + self.num_constraints + 1

        tableau = np.zeros((rows, cols))

        for i in range(self.num_constraints):
            for j in range(self.num_variables):
                tableau[i][j] = constraints[i][j]

        for i in range(self.num_constraints):
            tableau[i][self.num_variables + i] = 1

        for i in range(self.num_constraints):
            tableau[i][-1] = rhs[i]

        for j in range(self.num_variables):
            tableau[-1][j] = -objective[j]

        self.tableau = tableau

    def print_tableau(self):

        print("\nAktualna tablica Simplex:")
        print("-" * 70)

        for row in self.tableau:
            for value in row:
                print(f"{value:10.2f}", end=" ")
            print()

        print("-" * 70)

    def find_pivot_column(self):

        last_row = self.tableau[-1, :-1]

        min_value = np.min(last_row)

        if min_value >= 0:
            return None

        return np.argmin(last_row)

    def find_pivot_row(self, pivot_col):

        ratios = []

        for i in range(self.num_constraints):

            element = self.tableau[i][pivot_col]

            if element > 0:
                ratio = self.tableau[i][-1] / element
                ratios.append(ratio)
            else:
                ratios.append(np.inf)

        if min(ratios) == np.inf:
            return None

        return np.argmin(ratios)

    def pivot(self, pivot_row, pivot_col):

        pivot_element = self.tableau[pivot_row][pivot_col]

        self.tableau[pivot_row] = (
            self.tableau[pivot_row] / pivot_element
        )

        for i in range(len(self.tableau)):

            if i != pivot_row:

                factor = self.tableau[i][pivot_col]

                self.tableau[i] = (
                    self.tableau[i]
                    - factor * self.tableau[pivot_row]
                )

    def solve(self):

        iteration = 1

        while True:

            print(f"\nITERACJA {iteration}")
            self.print_tableau()

            pivot_col = self.find_pivot_column()

            if pivot_col is None:
                print("\nZnaleziono rozwiazanie optymalne.")
                break

            pivot_row = self.find_pivot_row(pivot_col)

            if pivot_row is None:
                print("\nProblem nieograniczony.")
                return

            print(
                f"Kolumna glowna: {pivot_col + 1}"
            )

            print(
                f"Wiersz glowny: {pivot_row + 1}"
            )

            self.pivot(pivot_row, pivot_col)

            iteration += 1

        self.show_solution()

    def show_solution(self):

        print("\n" + "=" * 60)
        print("WYNIK KONCOWY")
        print("=" * 60)

        solution = np.zeros(self.num_variables)

        for j in range(self.num_variables):

            column = self.tableau[:, j]

            ones = np.sum(np.isclose(column, 1))
            zeros = np.sum(np.isclose(column, 0))

            if ones == 1 and zeros == len(column) - 1:

                row = np.where(np.isclose(column, 1))[0][0]

                if row < self.num_constraints:
                    solution[j] = self.tableau[row][-1]

        for i in range(self.num_variables):

            print(
                f"x{i+1} = {solution[i]:.2f}"
            )

        print(
            f"\nWartosc funkcji celu = "
            f"{self.tableau[-1][-1]:.2f}"
        )

        print("=" * 60)


def example():

    solver = SimplexSolver()

    objective = [3, 2]

    constraints = [
        [1, 1],
        [1, 0],
        [0, 1]
    ]

    rhs = [4, 2, 3]

    solver.num_variables = 2
    solver.num_constraints = 3

    solver.build_tableau(
        objective,
        constraints,
        rhs
    )

    solver.solve()


def menu():

    while True:

        print("\n")
        print("=" * 60)
        print("1 - Wprowadz wlasny problem")
        print("2 - Uruchom przyklad")
        print("3 - Zakoncz")
        print("=" * 60)

        choice = input("Wybor: ")

        if choice == "1":

            solver = SimplexSolver()

            solver.create_problem()

            solver.solve()

        elif choice == "2":

            example()

        elif choice == "3":

            print("Koniec programu.")
            break

        else:

            print("Niepoprawna opcja.")


if __name__ == "__main__":
    menu()