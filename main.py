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