import numpy as np
from tabulate import tabulate
import random


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
        self.penalties = {'row': [], 'column': []}
        for i in range(self.tableau.couts.shape[0]):
            row = self.tableau.couts[i, :]
            sorted_row = np.sort(row[row != np.inf])  # trier les coûts qui ne sont pas infinis
            if len(sorted_row) >= 2:
                penalty = sorted_row[1] - sorted_row[0]  # calculer la différence entre les deux plus petits coûts
                self.penalties['row'].append((penalty, i))

        for j in range(self.tableau.couts.shape[1]):
            column = self.tableau.couts[:, j]
            sorted_column = np.sort(column[column != np.inf])  # trier les coûts qui ne sont pas infinis
            if len(sorted_column) >= 2:
                penalty = sorted_column[1] - sorted_column[0]  # calculer la différence entre les deux plus petits coûts
                self.penalties['column'].append((penalty, j))

    def select_and_adjust(self):
        supply = np.copy(self.tableau.offres)
        demand = np.copy(self.tableau.demandes)
        rows_processed = np.zeros_like(supply, dtype=bool)
        cols_processed = np.zeros_like(demand, dtype=bool)

        iteration = 0
        while np.any(supply > 0) and np.any(demand > 0):
            iteration += 1
            print(f"\nIteration {iteration}:")

            self.calculate_penalties()

            max_penalty = max(self.penalties['column'] + self.penalties['row'], key=lambda x: x[0])
            max_penalty_indices = [index for index in self.penalties['column'] + self.penalties['row'] if
                                   index[0] == max_penalty[0]]

            min_cost = np.inf
            min_cost_index = None
            for index in max_penalty_indices:
                if len(index) >= 3:
                    i, j = index[1], index[2]
                    if self.tableau.couts[i, j] < min_cost and not rows_processed[i] and not cols_processed[j]:
                        min_cost = self.tableau.couts[i, j]
                        min_cost_index = (i, j)

            if min_cost_index is None:
                break

            i, j = min_cost_index
            flow = min(supply[i], demand[j])
            print(f"Choix de la cellule ({i + 1}, {j + 1}) avec un coût de {min_cost} et un flux de {flow}")

            self.solution[i, j] += flow

            # Mark the row and column as processed
            rows_processed[i] = True
            cols_processed[j] = True

            # If the supply or demand for this cell is exhausted, set its cost to infinity
            if supply[i] == 0 or demand[j] == 0:
                self.tableau.couts[i, j] = np.inf

            print("Solution actuelle:")
            print(self.solution)

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
        print("Pénalités par ligne:")
        for penalty in self.penalties['row']:
            print(f"Ligne {penalty[1] + 1}: {penalty[0]}")

        print("Pénalités par colonne:")
        for penalty in self.penalties['column']:
            print(f"Colonne {penalty[1] + 1}: {penalty[0]}")

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
