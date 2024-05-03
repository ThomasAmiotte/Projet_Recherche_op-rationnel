# Lecture des données issues du fichier .txt et son stockage en mémoire
from tabulate import tabulate
from collections import deque


def read_file(file_name):
    tableau = []
    with open(file_name, 'r') as f:
        for line in f:
            tache = list(map(int, line.strip().split()))
            tableau.append(tache)
    return tableau


# Affichage des tableaux suivants
# Matrice des coûts
def afficher_matrice_couts(tableau):
    lignes_intermediaires = tableau[1:-1]
    matrice_couts = [ligne[:-1] for ligne in lignes_intermediaires]
    print("Voici la matrice des couts")
    print(tabulate(matrice_couts, tablefmt='grid'))
    return matrice_couts


# Proposition de transport (Nord-Ouest)
# 1.Extraction des offres
def afficher_offre(tableau):
    lignes_intermediaires = tableau[1:-1]
    offre = [ligne[-1] for ligne in lignes_intermediaires]
    return offre


# 2.Extraction des demandes
def afficher_demande(tableau):
    demande = tableau[-1]
    return demande


# NORD OUEST
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
    penalites_lignes = [(sorted(set(line))[1] - sorted(set(line))[0] if len(set(line)) > 1 else 0, 'ligne', i)
                        for i, line in enumerate(lignes)]
    penalites_colonnes = [(sorted(set(col))[1] - sorted(set(col))[0] if len(set(col)) > 1 else 0, 'colonne', i)
                          for i, col in enumerate(colonnes)]
    return penalites_lignes + penalites_colonnes


def find_max_penalty(all_penalities):
    return max(all_penalities, key=lambda x: x[0])


def count_max_penalty(all_penalities, penalite_max):
    return sum(1 for x in all_penalities if x[0] == penalite_max[0])


def select_min_cost_index(penalite_max, all_penalities, couts, offres, demandes):
    type_max, index_max = penalite_max[1], penalite_max[2]
    best_index = None
    best_cost = float('inf')

    if type_max == 'ligne':
        for j in range(len(demandes)):
            if demandes[j] > 0 and couts[index_max][j] < best_cost:
                best_index = j
                best_cost = couts[index_max][j]
    else:
        for i in range(len(offres)):
            if offres[i] > 0 and couts[i][index_max] < best_cost:
                best_index = i
                best_cost = couts[i][index_max]

    return best_index, best_cost


def update_costs(couts, i, j, increment=1):
    couts[i][j] += increment


def validate_solution(offres, demandes):
    return all(x == 0 for x in offres) and all(x == 0 for x in demandes)


def print_table(data, headers):
    print(tabulate(data, headers=headers, tablefmt="grid"))


def balas_hammer(offres, demandes, couts):
    solution = [[0] * len(demandes) for _ in range(len(offres))]
    costs_updated = [row[:] for row in couts]

    while True:
        lignes, colonnes = extract_rows_and_columns(costs_updated)
        penalites = calculate_penalties(costs_updated, lignes, colonnes)
        max_penalite = find_max_penalty(penalites)

        if max_penalite[0] == 0 or all(o == 0 for o in offres) or all(d == 0 for d in demandes):
            break  # Aucune pénalité significative ou toutes les offres/demandes sont satisfaites

        min_cost_index, min_cost_value = select_min_cost_index(max_penalite, penalites, costs_updated, offres, demandes)
        if min_cost_index is None or min_cost_index >= len(demandes) or max_penalite[2] >= len(offres):
            print("Aucun chemin viable trouvé ou indices hors limite.")
            break

        source_index = max_penalite[2] if max_penalite[1] == 'ligne' else min_cost_index
        target_index = min_cost_index if max_penalite[1] == 'ligne' else max_penalite[2]

        quantite = min(offres[source_index], demandes[target_index])
        if quantite > 0:
            solution[source_index][target_index] += quantite
            offres[source_index] -= quantite
            demandes[target_index] -= quantite
            update_costs(costs_updated, source_index, target_index)
        else:
            print("Aucune quantité significative à transporter, arrêt de l'algorithme.")
            break

        print(f"Transport de {quantite} unités de {source_index} à {target_index}")
        print(f"Offres restantes: {offres}, Demandes restantes: {demandes}")

    print("Solution finale:")
    print(tabulate(solution, tablefmt='grid'))
    return solution


def update_costs_matrix(couts, solution, offres, demandes):
    """Met à jour les coûts et les quantités restantes dans les offres et demandes après chaque itération de transport."""
    n = len(offres)
    m = len(demandes)

    # Mise à jour des offres et demandes
    for i in range(n):
        for j in range(m):
            transported = solution[i][j]
            if transported > 0:
                # Soustraire la quantité transportée des offres et des demandes
                offres[i] -= transported
                demandes[j] -= transported
                # Assurez-vous que la quantité ne devienne pas négative
                offres[i] = max(offres[i], 0)
                demandes[j] = max(demandes[j], 0)

                # Mettre à jour les coûts (si nécessaire, par exemple en augmentant légèrement le coût pour éviter la réutilisation de cette route)
                # Cela pourrait être une stratégie pour empêcher l'algorithme de choisir la même route indéfiniment si plusieurs solutions sont possibles.
                couts[i][
                    j] += 1  # Augmente le coût pour rendre cette route moins attrayante pour les itérations futures


def update_transport(offres, demandes, max_penalite, min_cost_index, couts):
    # Vérification si les indices sont dans les limites des listes offres et demandes avant toute manipulation
    if max_penalite[2] >= len(offres) or min_cost_index >= len(demandes):
        print(f"Index out of range: max_penalite[2]={max_penalite[2]}, min_cost_index={min_cost_index}")
        return [], False  # Retourner une solution vide et False pour indiquer l'arrêt

    print(f"Starting transport - Offre Index: {max_penalite[2]}, Demande Index: {min_cost_index}")
    quantite = min(offres[max_penalite[2]], demandes[min_cost_index])
    print(f"Quantité à transporter: {quantite}")

    solution = [[0] * len(demandes) for _ in range(len(offres))]
    solution[max_penalite[2]][min_cost_index] = quantite
    offres[max_penalite[2]] -= quantite
    demandes[min_cost_index] -= quantite

    # Affiche l'état des offres et demandes après transport
    print(f"Remaining Offers: {offres}")
    print(f"Remaining Demands: {demandes}")

    # Retourner la solution partielle et un booléen indiquant si le transport a été possible
    return solution, True if quantite > 0 else False


def calcul_cout_total(couts, solution):
    total = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            total += solution[i][j] * couts[i][j]
    return total


# Savoir si la proposition est acyclique ou non
def iscycle(graph):
    visited = set()  # Un set pour sotcké les noeuds visités
    parent = {}  # Dictionnaire pour garder une trace des parents des sommets

    # Fonction de parcours en largeur
    def bfs(start):
        queue = deque([start])
        visited.add(start)
        parent[start] = None  # Le sommet de départ n'a pas de parent
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
                elif parent[current] != neighbor:
                    # Un cycle a été détécté
                    return True, current, neighbor
        return False, None, None


def find_cycle(start, end, parent):
    cycle = []
    cycle.append(start)
    while start != end:
        start = parent[start]
        cycle.append(start)
        cycle.append(end)
        cycle.reverse()
        return cycle


