import copy

import numpy as np
from tabulate import tabulate
import random


class BalasHammer:
    def __init__(self, tableau):
        self.penalties = None
        self.tableau = tableau
        self.solution = np.full((tableau.couts.shape[0],tableau.couts.shape[1]), fill_value=None)

    def display_matrix_tabulate(self, matrix, title="Matrix"):
        print(title + ":\n" + tabulate(matrix, tablefmt="fancy_grid", headers="keys", showindex="always"))

    def display_matrix_brackets(self, matrix, title="Matrix"):
        print(title + " as list:")
        print(matrix.tolist())

    def calculate_penalties(self,cost_copy):
        print("Cost copy de la fonction")
        print(cost_copy)
        penalties = {'row': [], 'column': []}
        if np.all(np.isinf(cost_copy)):
            return None
        else:
            for i in range(cost_copy.shape[0]):
                row = cost_copy[i, :]
                sorted_row = np.sort(row[row != np.inf])  # trier les coûts qui ne sont pas infinis
                print("Sorted Row")
                print(sorted_row)
                if len(sorted_row) >= 2:
                    penalty = sorted_row[1] - sorted_row[0]  # calculer la différence entre les deux plus petits coûts
                    penalties['row'].append((penalty, i))
                elif len(sorted_row)==1:
                    penalty= sorted_row[0]
                    penalties['row'].append((penalty, i))

            for j in range(cost_copy.shape[1]):
                column = cost_copy[:, j]
                sorted_column = np.sort(column[column != np.inf])  # trier les coûts qui ne sont pas infinis
                print("Sorted column")
                print(sorted_column)
                if (len(sorted_column)) != 0:
                    if len(sorted_column) >= 2:
                        penalty = sorted_column[1] - sorted_column[0]  # calculer la différence entre les deux plus petits coûts
                        penalties['column'].append((penalty, j))
                    elif len(sorted_column)==1:
                        penalty= sorted_column[0]
                        penalties['column'].append((penalty, j))
        return penalties

    def select_and_adjust(self):
        offer_copy = copy.deepcopy(self.tableau.offres)
        demand_copy = copy.deepcopy(self.tableau.demandes)
        cost_copy = copy.deepcopy(self.tableau.couts.astype(float))
        while True:
            penalities = self.calculate_penalties(cost_copy)
            if(penalities==None):
                break
            row_index=None
            column_index=None
            max_penalty = -1
            for i in penalities['row']:
                if i[0]>max_penalty:
                    max_penalty=i[0]
                    row_index=i[1]

            for i in penalities['column']:
                if i[0]>max_penalty:
                    max_penalty=i[0]
                    column_index=i[1]
                    row_index=None

            minimal_cost=np.inf
            if column_index==None:
                for i in range(len(cost_copy[row_index])):
                    if cost_copy[row_index][i]<minimal_cost:
                        minimal_cost=cost_copy[row_index][i]
                        column_index=i
            else:
                for i in range(len(cost_copy)):
                    if cost_copy[i,column_index]<minimal_cost:
                        minimal_cost=cost_copy[i,column_index]
                        row_index = i

            quantity_max = min(offer_copy[row_index],demand_copy[column_index])
            self.solution[row_index][column_index] = quantity_max
            #Si la quantité max est détectée parmi les offres / donc on va procéder le long de la ligne
            if(offer_copy[row_index]==quantity_max):
                #On va mettre une quantité qui correspond à l'offre max, donc l'offre dispo passe à 0
                offer_copy[row_index]=0
                # On enlève la quantité qu'on ajoute dans le tableau à la demande sur la colonne correspondante
                demand_copy[column_index]= demand_copy[column_index]-quantity_max

                #On a maximisé la quantité par rapport à l'offre, donc le reste de la ligne passe à 0 (si jamais modifiée)
                for i in range(len(self.solution[0])):
                    if self.solution[row_index][i]==None:
                        self.solution[row_index][i]=0
                    cost_copy[row_index][i]=np.inf

                #Dans le cas où l'offre et la demande sont toutes les deux maximisées, on remplis aussi la colonne de 0
                if demand_copy[column_index]==0:
                    for i in range(len(self.solution)):
                        if self.solution[i][column_index]==None:
                            self.solution[i][column_index]=0
                        cost_copy[i][column_index] = np.inf

            elif(demand_copy[column_index]==quantity_max):
                demand_copy[column_index] = 0
                offer_copy[row_index] = offer_copy[row_index] - quantity_max
                for i in range(len(self.solution)):
                    if self.solution[i][column_index] == None:
                        self.solution[i][column_index] = 0
                    cost_copy[i][column_index] = np.inf



            print("Cost copie")
            print(cost_copy)
            print("Solution actuelle")
            print(self.solution)
        print("Solution actuelle")
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
                self.solution[i][j] = flow
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
        self.select_and_adjust()
        # Vérification que toute l'offre et la demande ont été complètement utilisées
        if not np.all(self.tableau.offres == 0) or not np.all(self.tableau.demandes == 0):
            print("Erreur: Toute l'offre ou la demande n'a pas été complètement utilisée.")
        print("Solution finale:")
        self.display_matrix_tabulate(self.solution, "Solution Balas-Hammer")
        total_cost = np.sum(self.solution * self.tableau.couts)
        print("Coût total de la solution:", total_cost)
        self.tableau.check_supply_demand()
