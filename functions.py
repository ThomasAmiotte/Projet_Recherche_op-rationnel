#Lecture des données issues du fichier .txt et son stockage en mémoire
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
    for ligne in matrice_couts:
        print(ligne)

#Proposition de transport (Nord-Ouest)
#1.Extraction des offres
def afficher_offre(tableau):
    lignes_intermediaires = tableau[:1]
    offre = [ligne[-1] for ligne in lignes_intermediaires]
    for ligne in offre:
        print(ligne)
#2.Extraction des demandes
def afficher_demande(tableau):
    demande = tableau[-1]
    print(demande)

#NORD OUEST
def coin_nord_ouest(offres, demandes, couts):
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

        # Avancer dans la matrice
        if offres[i] == 0 and i < len(offres) - 1:
            i += 1
        elif demandes[j] == 0 and j < len(demandes) - 1:
            j += 1

    return solution


# Exemple d'utilisation
offres = [20, 30, 25]  # Quantités disponibles dans chaque source
demandes = [25, 25, 25]  # Quantités requises par chaque destination
couts = [
    [8, 6, 10],
    [9, 7, 4],
    [3, 4, 2]
]  # Matrice des coûts de transport

solution = coin_nord_ouest(offres, demandes, couts)
for ligne in solution:
    print(ligne)
