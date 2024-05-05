from BalasHammer import BalasHammer
from TableauTransport import TransportTableau


def main():
    # Liste de tous les fichiers de tableau à traiter
    tableau_files = [
        "tableau/table5.txt"
    ]

    for file_path in tableau_files:
        print(f"Traitement du fichier {file_path}")
        tableau = TransportTableau(file_path)
        balas_hammer = BalasHammer(tableau)

        # Trouver une solution initiale avec l'angle nord-ouest comme point de départ pour Balas-Hamme
        tableau.display_all_matrices()


        # Exécution de la nouvelle méthode select_and_adjust
        balas_hammer.select_and_adjust()

        # Calculer et afficher le coût total
        cost = tableau.calculate_total_cost()
        print(f"Coût total de la solution: {cost}")

        # Vérifier la conformité de l'offre et de la demande
        tableau.check_supply_demand()

        # Séparation visuelle entre les traitements de fichiers
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()