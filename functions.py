#Lecture des données issues du fichier .txt et son stockage en mémoire
from tabulate import tabulate
from collections import deque

def read_file(file_name):
    tableau = []
    with open(file_name, 'r') as f:
        for line in f:
            tache = list(map(int, line.strip().split()))
            tableau.append(tache)
    return tableau
#Affichage des tableaux suivants
#Matrice des coûts
def afficher_matrice_couts(tableau):
    lignes_intermediaires = tableau[1:-1]
    matrice_couts = [ligne[:-1] for ligne in lignes_intermediaires]
    print("Voici la matrice des couts")
    print(tabulate(matrice_couts, tablefmt='grid'))
    return matrice_couts

#Proposition de transport (Nord-Ouest)
#1.Extraction des offres
def afficher_offre(tableau):
    lignes_intermediaires = tableau[1:-1]
    offre = [ligne[-1] for ligne in lignes_intermediaires]
    return offre
#2.Extraction des demandes
def afficher_demande(tableau):
    demande = tableau[-1]
    return demande
#NORD OUEST
def coin_nord_ouest(offres, demandes, couts):
    # Copie les listes pour éviter de modifier les originales
    offres = offres[:]
    demandes = demandes[:]

    # Initialiser la solution de transport avec des zéros
    solution = [[0] * len(demandes) for _ in range(len(offres))]
    i, j = 0, 0  # indices pour parcourir les lignes et les colonnes

    # Tant qu'il reste des offres et des demandes à satisfaire
    while i < len(offres) and j < len(demandes):
        # Trouver la quantité à transporter
        quantite = min(offres[i], demandes[j])
        solution[i][j] = quantite
        offres[i] -= quantite
        demandes[j] -= quantite

        # Avancer dans la matrice correctement
        if offres[i] == 0:
            i += 1
        if demandes[j] == 0:
            j += 1
    print("Voici la proposition NORD OUEST :")
    print(tabulate(solution, tablefmt='grid'))
    return solution
def extract_rows_and_columns(couts):
    lignes = couts
    colonnes = [list(colonne) for colonne in zip(*couts)]
    return lignes, colonnes

def calculate_penalties(couts, lignes, colonnes):
    penalites_lignes = [(sorted(line)[1] - sorted(line)[0], 'ligne', i) for i, line in enumerate(lignes)]
    penalites_colonnes = [(sorted(col)[1] - sorted(col)[0], 'colonne', i) for i, col in enumerate(colonnes)]
    all_penalities = penalites_lignes + penalites_colonnes
    return all_penalities

def find_max_penalty(all_penalities):
    return max(all_penalities, key=lambda x: x[0])

def count_max_penalty(all_penalities, penalite_max):
    return sum(1 for x in all_penalities if x[0] == penalite_max[0])

def select_min_cost_index(penalite_max, all_penalities, couts):
    type_max, index_max = penalite_max[1], penalite_max[2]
    min_cost_index = None
    min_cost_value = float('inf')
    for penalite in all_penalities:
        if penalite[0] == penalite_max[0]:
            if penalite[1] == 'ligne':
                index = penalite[2]
                min_value = min(couts[index])
            else:
                index = penalite[2]
                min_value = min([ligne[index] for ligne in couts])
            if min_value < min_cost_value:
                min_cost_index = index
                min_cost_value = min_value
    return min_cost_index, min_cost_value

def remove_row_or_column(couts, index, type_element):
    if type_element == 'ligne':
        #Suppression d'une ligne
        return [row for i, row in enumerate(couts) if i !=index]
    else:
        #Suppression d'une colonne
        return [row[:index] + row[index + 1:] for row in couts]

def balas_hammer(offres, demandes, couts):
    # Extraction des lignes et des colonnes
    lignes, colonnes = extract_rows_and_columns(couts)

    # Calcul des pénalités pour chaque ligne et colonne
    all_penalities = calculate_penalties(couts, lignes, colonnes)

    # Trouver la pénalité maximale
    penalite_max = find_max_penalty(all_penalities)

    # Compter le nombre d'occurrences de la pénalité maximale
    count_max = count_max_penalty(all_penalities, penalite_max)

    print("La penalite max est ", penalite_max)
    print(all_penalities)

    if count_max >= 2:
        min_cost_index, min_cost_value = select_min_cost_index(penalite_max, all_penalities, couts)
        if min_cost_index is not None:
            if penalite_max[1] == 'ligne':
                quantite = min(offres[penalite_max[2]], demandes[min_cost_index])
                solution = [[0] * len(demandes) for _ in range(len(offres))]
                solution[penalite_max[2]][min_cost_index] = quantite
                offres[penalite_max[2]] -= quantite
                demandes[min_cost_index] -= quantite
            else:
                quantite = min(offres[min_cost_index], demandes[penalite_max[2]])
                solution = [[0] * len(demandes) for _ in range(len(offres))]
                solution[min_cost_index][penalite_max[2]] = quantite
                offres[min_cost_index] -= quantite
                demandes[penalite_max[2]] -= quantite
    else:
        min_cost_index, min_cost_value = select_min_cost_index(penalite_max, all_penalities, couts)
        if min_cost_index is not None:
            if penalite_max[1] == 'ligne':
                quantite = min(offres[penalite_max[2]], demandes[min_cost_index])
                solution = [[0] * len(demandes) for _ in range(len(offres))]
                solution[penalite_max[2]][min_cost_index] = quantite
                offres[penalite_max[2]] -= quantite
                demandes[min_cost_index] -= quantite
            else:
                quantite = min(offres[min_cost_index], demandes[penalite_max[2]])
                solution = [[0] * len(demandes) for _ in range(len(offres))]
                solution[min_cost_index][penalite_max[2]] = quantite
                offres[min_cost_index] -= quantite
                demandes[penalite_max[2]] -= quantite

    print("La matrice des couts après balas-hammer")
    print(tabulate(solution, tablefmt='grid'))
    return solution


def calcul_cout_total(couts, solution):
    total = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            total += solution[i][j] * couts[i][j]
    return total

#Savoir si la proposition est acyclique ou non

from collections import deque


def detect_cycle_bfs(graph):
    n = len(graph)  # Nombre de sommets dans le graphe
    visited = [False] * n  # Marquer les sommets visités
    parent = [-1] * n  # Parent de chaque sommet dans l'arbre de parcours

    def bfs(source):
        queue = deque([source])
        visited[source] = True

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if not visited[neighbor]:  # Si le voisin n'a pas été visité
                    visited[neighbor] = True
                    parent[neighbor] = node
                    queue.append(neighbor)
                elif parent[node] != neighbor:  # Détection d'un cycle
                    # Reconstruction du cycle
                    cycle = []
                    # Remonter à partir de node jusqu'à trouver le cycle
                    current = node
                    while current != -1 and current != neighbor:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(neighbor)
                    cycle.append(node)
                    cycle.reverse()
                    return cycle
        return None

    # Exécuter BFS à partir de chaque sommet non visité
    for i in range(n):
        if not visited[i]:
            result = bfs(i)
            if result:
                return result  # Retourner le premier cycle trouvé

    return "No cycle found"  # Aucun cycle trouvé

"""
def find_cycle(start,end,parent):
    cycle = []
    cycle.append(start)
    while start != end:
        start = parent[start]
        cycle.append(start)
        cycle.append(end)
        cycle.reverse()
        return cycle
has_cycle, cycle = detect_cycle(graph)
if has_cycle:
    print("Cycle detected:", cycle)
else:
    print("No cycle detected")
    """