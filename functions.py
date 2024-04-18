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
    print("Voici la matrice des couts")
    for ligne in matrice_couts:
        print(ligne)
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
    return solution

def balas_hammer(offres, demandes, couts):
    #extraction de chaque ligne
    for ligne in couts:
        print(ligne)
    #extraction de chaque colonne
    colonnes = [list(colonne) for colonne in zip(*couts)]
    for colonne in colonnes:
        print(colonne)
    #Collecter les pénalités pour toutes les colonnes
    penalites_colonnes  = []
    mins_col = [sorted(colonne)[:2] for colonne in colonnes]
    for i, mins in enumerate(mins_col):
        penalite_colonne = mins[1] - mins[0]
        print(f"Les deux minimum de la colonne sont", mins)
        print("La penalyté sur cette colonne est de ", mins[1] - mins[0])
        penalites_colonnes.append((penalite_colonne, 'colonne', i))
    lines = [line for line in couts]
    penalites_lignes = []
    mins_line = [sorted(line)[:2] for line in lines]
    for i, mins in enumerate(mins_line):
        penalite_ligne = mins[1] - mins[0]
        print(f"Les deux minimum de la ligne sont", mins)
        print("La penalyté sur cette ligne est de ", mins[1] - mins[0])
        penalites_lignes.append((penalite_ligne, 'ligne', i))
    #Trouver la penalité la plus élevé
    all_penalities = penalites_lignes + penalites_colonnes
    penalite_max = max(all_penalities, key=lambda x: x[0])
    print("La penalite max est ", penalite_max)