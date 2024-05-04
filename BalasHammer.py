import numpy as np
from tabulate import tabulate


class BalasHammer:
    def __init__(self, tableau):
        self.penalties = None
        self.tableau = tableau
        self.solution = np.zeros_like(self.tableau.couts)

    def display_matrix_tabulate(self, matrix, title="Matrix"):
        print(title + ":\n" + tabulate(matrix, tablefmt="fancy_grid", headers="keys", showindex="always"))

    def display_matrix_brackets(self, matrix, title="Matrix"):
        print(title + " as list:")
        print(matrix.tolist())

    def minimum_cost_method(self):
        # Crée des copies des tableaux d'offre et de demande
        offres_copy = np.copy(self.tableau.offres)
        demandes_copy = np.copy(self.tableau.demandes)

        # Continue jusqu'à ce que l'offre et la demande soient complètement épuisées
        while np.any(offres_copy > 0) and np.any(demandes_copy > 0):
            # Trouve la cellule avec le coût le plus bas
            min_cost = np.min(self.tableau.couts)
            min_cost_indices = np.where(self.tableau.couts == min_cost)

            for index in zip(min_cost_indices[0], min_cost_indices[1]):
                i, j = index
                # Allocation basée sur le minimum de l'offre ou de la demande restante
                quantity = min(offres_copy[i], demandes_copy[j])
                self.solution[i, j] += quantity
                offres_copy[i] -= quantity
                demandes_copy[j] -= quantity

                # Si l'offre ou la demande de cette cellule est épuisée, mettez son coût à l'infini
                if offres_copy[i] == 0 or demandes_copy[j] == 0:
                    self.tableau.couts[i, j] = np.inf

    def calculate_penalties(self):
        # Calcul des pénalités pour chaque ligne et chaque colonne
        self.penalties = {'row': [], 'column': []}
        for i, row in enumerate(self.tableau.couts):
            sorted_costs = np.sort(np.unique(row))
            if len(sorted_costs) > 1:
                self.penalties['row'].append((sorted_costs[1] - sorted_costs[0], i))

        for j in range(self.tableau.couts.shape[1]):
            column = self.tableau.couts[:, j]
            sorted_costs = np.sort(np.unique(column))
            if len(sorted_costs) > 1:
                self.penalties['column'].append((sorted_costs[1] - sorted_costs[0], j))

    def select_and_adjust(self):
        # Crée des copies des tableaux d'offre et de demande
        offres_copy = np.copy(self.tableau.offres)
        demandes_copy = np.copy(self.tableau.demandes)

        # Continue jusqu'à ce que l'offre et la demande soient complètement épuisées
        while np.any(offres_copy > 0) and np.any(demandes_copy > 0):
            # Calcule les pénalités pour chaque ligne et colonne
            self.calculate_penalties()

            # Sélectionne la ligne ou la colonne où la pénalité est maximale
            max_penalty = max(self.penalties['column'] + self.penalties['row'], key=lambda x: x[0], default=(0, -1, -1))
            if max_penalty[1] == -1:
                break  # Aucune pénalité trouvée, probablement une erreur de logique

            # Trouve toutes les lignes/colonnes avec la pénalité maximale
            max_penalty_indices = [index for index in self.penalties['column'] + self.penalties['row'] if
                                   index[0] == max_penalty[0]]

            # S'il y a plusieurs lignes/colonnes avec la même pénalité maximale
            if len(max_penalty_indices) > 1:
                # Choisissez la ligne/colonne dont la cellule de coût minimal a la capacité maximale
                max_capacity = -1
                for index in max_penalty_indices:
                    i, j = index[1], index[2]
                    capacity = min(offres_copy[i], demandes_copy[j])
                    if capacity > max_capacity:
                        max_capacity = capacity
                        max_penalty = index

            i, j = max_penalty[1], max_penalty[2]
            # Allocation basée sur le minimum de l'offre ou de la demande restante
            quantity = min(offres_copy[i], demandes_copy[j])
            self.solution[i, j] += quantity
            offres_copy[i] -= quantity
            demandes_copy[j] -= quantity

            # Si l'offre ou la demande de cette cellule est épuisée, mettez son coût à l'infini
            if offres_copy[i] == 0 or demandes_copy[j] == 0:
                self.tableau.couts[i, j] = np.inf

    def find_initial_solution(self):
        # Implémentation de l'algorithme Balas-Hammer pour trouver la solution initiale
        # Cette implémentation est hypothétique et doit être adaptée à vos besoins spécifiques
        self.corner_north_west()
        print("Solution initiale trouvée en utilisant Balas-Hammer:")
        self.display_matrix_tabulate(self.solution, "Solution Balas-Hammer")
        self.display_matrix_brackets(self.solution, "Solution Balas-Hammer")

    def corner_north_west(self):
        # Implémentation simplifiée de l'angle nord-ouest
        supply = np.copy(self.tableau.offres)
        demand = np.copy(self.tableau.demandes)
        for i in range(len(supply)):
            for j in range(len(demand)):
                if supply[i] == 0 or demand[j] == 0:
                    continue
                flow = min(supply[i], demand[j])
                self.solution[i, j] = flow
                supply[i] -= flow
                demand[j] -= flow

    def display_penalties(self):
        print("Pénalités par cellule:")
        print(self.penalties)

    def execute(self):
        self.find_initial_solution()
        self.select_and_adjust()
        # Vérification que toute l'offre et la demande ont été complètement utilisées
        if not np.all(self.tableau.offres == 0) or not np.all(self.tableau.demandes == 0):
            print("Erreur: Toute l'offre ou la demande n'a pas été complètement utilisée.")
        print("Solution finale:")
        self.display_matrix_tabulate(self.solution, "Solution Balas-Hammer")
        total_cost = np.sum(self.solution * self.tableau.couts)
        print("Coût total de la solution:", total_cost)
        self.tableau.check_supply_demand()
