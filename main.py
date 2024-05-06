from BalasHammer import BalasHammer
from TableauTransport import TransportTableau


def main():
    while True:
        print("\nMenu:")
        print("Veuillez choisir un nombre entre 1 et 12.")
        print("0. Quitter")

        choice = input("Quelle table voulez-vous lancer ? ")

        if choice == '0':
            break

        if not choice.isdigit() or int(choice) < 1 or int(choice) > 12:
            print("Choix invalide. Veuillez réessayer.")
            continue

        file_path = f"tableau/table{choice}.txt"
        print(f"Traitement du fichier {file_path}")
        tableau = TransportTableau(file_path)

        # Trouver une solution initiale avec l'angle nord-ouest
        tableau.corner_north_west()
        tableau.display_all_matrices()

        # Création d'une instance de la classe BalasHammer
        balas_hammer = BalasHammer(tableau)

        # Exécution de la nouvelle méthode select_and_adjust
        balas_hammer.execute()

        # Séparation visuelle entre les traitements de fichiers
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
