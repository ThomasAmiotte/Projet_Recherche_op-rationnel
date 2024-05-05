"""
from functions import *
tableau = read_file("tableau/table1.txt")
print(tableau)
afficher_demande(tableau)
afficher_matrice_couts(tableau)
print("Bienvenue dans le système de sélection de transport !")
print("Voici les options disponibles :")
print("1. NORD OUEST - Le trajet rapide vers le nord-ouest.")
print("2. Ballas Hammer - L'expérience ultime de confort et de luxe.")
# Boucle jusqu'à ce que l'utilisateur entre une option valide
while True:
    choix = input("Veuillez entrer votre choix (1 ou 2) :\n")
    if choix in ['1', '2']:
        print(f"Vous avez choisi l'option {choix}. Merci !")
        if choix == '1':
            couts = afficher_matrice_couts(tableau)
            offres = afficher_offre(tableau)
            demandes = afficher_demande(tableau)
            print("Offres", offres, "Demandes", demandes)
            print(coin_nord_ouest(offres, demandes, couts))
    else:
        print("Entrée invalide. Veuillez choisir entre 1 et 2.\n")
"""
import random
import time
from functions import *
tableau = read_file("tableau/table1.txt")
couts = afficher_matrice_couts(tableau)
print("Voici les offres")
offres = afficher_offre(tableau)
print(offres)
print("Voici les demandes")
demandes = afficher_demande(tableau)
print(demandes)
print("Voici la proposition apres Balas-Hammer")
balas_hammer(offres, demandes, couts)

graph = [
    [1, 2],
    [0, 2],
    [0, 1, 3],
    [2, 4],
    [3]
]

print(detect_cycle_bfs(graph))


### LES PROBLÈMES DE TRANSPORT EN ENTRÉE ###

def generate_random_transport_problem(n):
    # Initialiser la matrice A avec des zéros
    A = [[0 for _ in range(n)] for _ in range(n)]

    # Générer un nombre aléatoire entre 1 et 100 pour chaque élément de la matrice
    for i in range(n):
        for j in range(n):
            A[i][j] = random.randint(1, 100)

    return A

def generer_matrice(n):
    matrice = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    return matrice

def calculer_provisions_et_commandes(matrice):
    n = len(matrice)
    provisions = [sum(ligne) for ligne in matrice]
    commandes = [sum(matrice[i][j] for i in range(n)) for j in range(n)]
    return provisions, commandes

# Exemple d'utilisation
n = 5  # Taille de la matrice
matrice = generer_matrice(n)
print("Matrice:")
for ligne in matrice:
    print(ligne)

provisions, commandes = calculer_provisions_et_commandes(matrice)
print("\nSomme des provisions:", provisions)
print("Somme des commandes:", commandes)

### LA MESURE DU TEMPS ###

### MESURE DU TEMPS NORD OUEST ###

n = max(len(offres), len(demandes))  # Taille des listes offres et demandes

start_time = time.perf_counter()
result = coin_nord_ouest(offres, demandes, couts)
end_time = time.perf_counter()

execution_time = end_time - start_time
print("Temps d'exécution de l'algorithme Nord-Ouest (θNO(n)):", execution_time, "secondes")


def generate_random_transport_problem(n):
    # Générer des valeurs aléatoires pour les coûts
    cost = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    # Générer des valeurs aléatoires pour les offres et les demandes
    supp = [random.randint(1, 100) for _ in range(n)]
    demandes = [random.randint(1, 100) for _ in range(n)]
    return cost, supp, demandes