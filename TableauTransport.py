import numpy as np
from tabulate import tabulate


class TransportTableau:
    def __init__(self, file_path):
        self.file_path = file_path
        self.couts, self.offres, self.demandes = self.read_file()
        self.solution = np.zeros_like(self.couts)

    def read_file(self):
        with open(self.file_path, 'r') as file:
            next(file)  # Skip the first line (header with dimensions)
            lines = file.readlines()
            costs = []
            offres = []
            # Read cost matrix lines and offers
            for line in lines[:-1]:  # Skip last line because it's demands
                parts = list(map(int, line.strip().split()))
                costs.append(parts[:-1])
                offres.append(parts[-1])
            # Last line is demands
            demandes = list(map(int, lines[-1].strip().split()))
        costs = np.array(costs, dtype=int)
        offres = np.array(offres, dtype=int)
        demandes = np.array(demandes, dtype=int)  # Assume the last element is not needed if it's zero or redundant
        return costs, offres, demandes

    def display_matrix(self, matrix, title="Matrix", headers=None):
        if headers is None:
            headers = [str(i + 1) for i in range(matrix.shape[1])]
        row_labels = [str(i + 1) for i in range(matrix.shape[0])]
        print(title + ":")
        print(tabulate(matrix, headers=headers, showindex=row_labels, tablefmt='fancy_grid'))

    def display_all_matrices(self):
        self.display_matrix(self.couts, "Matrice des Coûts")
        self.display_matrix(self.solution, "Proposition de Transport")
        print("Offres:", self.offres)
        print("Demandes:", self.demandes)

    def corner_north_west(self):
        supply = np.copy(self.offres)
        demand = np.copy(self.demandes)
        for i in range(len(supply)):
            for j in range(len(demand)):
                if supply[i] == 0 and demand[j] == 0:
                    continue
                flow = min(supply[i], demand[j])
                self.solution[i, j] = flow
                supply[i] -= flow
                demand[j] -= flow

    def calculate_total_cost(self):
        total_cost = 0
        for i in range(self.solution.shape[0]):
            for j in range(self.solution.shape[1]):
                total_cost += self.solution[i, j] * self.couts[i, j]
        return total_cost

