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
"""from functions import *
tableau = read_file("tableau/table1.txt")
couts = afficher_matrice_couts(tableau)
print("Voici les offres")
offres = afficher_offre(tableau)
print(offres)
print("Voici les demandes")
demandes = afficher_demande(tableau)
print(demandes)
print("Voici la proposition apres Balas-Hammer")
balas_hammer(offres, demandes, couts)"""

from functions import *


"""def main():
    # Lecture du fichier et extraction des données
    print("Lecture des données...")
    tableau = read_file("tableau/table5.txt")

    # Affichage de la matrice des coûts
    print("Extraction et affichage de la matrice des coûts...")
    couts = afficher_matrice_couts(tableau)

    # Extraction des offres et des demandes
    print("Extraction des offres...")
    offres = afficher_offre(tableau)
    print("Offres:", offres)

    print("Extraction des demandes...")
    demandes = afficher_demande(tableau)
    print("Demandes:", demandes)

    # Exécution de l'algorithme Balas-Hammer
    print("Exécution de l'algorithme Balas-Hammer...")
    solution = balas_hammer(offres, demandes, couts)
    print("Solution optimale trouvée par Balas-Hammer:")
    print(solution)


if __name__ == "__main__":
    main()
"""


def main():
    base_path = "tableau/"
    tableau_files = [
        "table1.txt", "table2.txt", "table3.txt", "table4.txt",
        "table5.txt", "table6.txt", "table7.txt", "table8.txt",
        "table9.txt", "table10.txt", "table11.txt", "table12.txt",
    ]

    for file_name in tableau_files:
        full_path = base_path + file_name
        print(f"Lecture des données pour {file_name}...")
        tableau = read_file(full_path)

        print("Extraction et affichage de la matrice des coûts...")
        couts = afficher_matrice_couts(tableau)

        print("Extraction des offres...")
        offres = afficher_offre(tableau)
        print("Offres:", offres)

        print("Extraction des demandes...")
        demandes = afficher_demande(tableau)
        print("Demandes:", demandes)

        print("Exécution de l'algorithme Balas-Hammer...")
        solution = balas_hammer(offres, demandes, couts)

        # Calcul et affichage du coût total de la solution
        cout_total = calcul_cout_total(couts, solution)
        print("Solution optimale trouvée par Balas-Hammer pour", file_name, ":")
        print(solution)
        print("Coût total de la solution :", cout_total)
        print("\n" + "-" * 60 + "\n")  # Séparateur pour chaque résultat


if __name__ == "__main__":
    main()

