



import copy
class Graphe:
    def __init__(self,cost_tab,tab_quantity):
        self.adj_list = {}
        self.cost_tab = cost_tab
        self.tab_quantity = tab_quantity

    def ajoute_arete(self, src, dest, cout, quantite):
        if src not in self.adj_list:
            self.adj_list[src] = []
        if dest not in self.adj_list:
            self.adj_list[dest] = []
        self.adj_list[src].append((dest, cout, quantite))
        self.adj_list[dest].append((src, cout, quantite))  # Ajouter aussi l'arête inverse pour le graphe non orienté
    
    def est_cyclique(self):
        visited = set()

        def visite(noeud, parent):
            visited.add(noeud)
            for voisin, _, _ in self.adj_list.get(noeud, []):
                if voisin not in visited:
                    if visite(voisin, noeud):
                        return True
                elif voisin != parent:
                    return True
            return False

        for n in self.adj_list:
            if n not in visited:
                if visite(n, None):
                    return True
        return False

    def est_connexe(self):
        if not self.adj_list:
            return True

        def parcours_dfs(noeud, visited):
            visited.add(noeud)
            for voisin, _, _ in self.adj_list.get(noeud, []):
                if voisin not in visited:
                    parcours_dfs(voisin, visited)

        visited = set()
        # Commencer le parcours à partir d'un nœud arbitraire (le premier dans l'adj_list)
        parcours_dfs(next(iter(self.adj_list)), visited)
        return len(visited) == len(self.adj_list)
# Utilisation de la classe Graphe



tab_cost = [[10,5,5,3],[10,4,5,5],[4,4,3,5]]
tab_quantity = [[6,0,6,0],[0,12,0,0],[0,0,3,9]]
g = Graphe(tab_cost,tab_quantity)

for y,ligne in enumerate(tab_quantity):
    for x,tab_quantity_ele in enumerate(ligne):
        if tab_quantity_ele:
            g.ajoute_arete(str(chr(83)+str(y+1)),str("T"+chr(65+x)),tab_cost[y][x],tab_quantity_ele)
print(g.adj_list)


def connexe(g:Graphe):
    temp : Graphe = None
    # renvoie les cout sans doublons et trié
    liste_fusionnee = [item for sublist in tab_cost for item in sublist]
    sorted_cost = sorted(set(liste_fusionnee))
    for i in sorted_cost: # on cherche en premier les élèment avec les prix les plus bas
        for y,ligne in enumerate(tab_quantity):
            for x,tab_quantity_ele in enumerate(ligne):
                if tab_quantity_ele==0 and tab_cost[y][x]==i: # il n'existe pas de chemin
                    #print("on ajoute",str(chr(83)+str(y+1)),str("T"+chr(65+x)),tab_cost[y][x],tab_quantity_ele)
                    temp = copy.deepcopy(g)
                    temp.ajoute_arete(str(chr(83)+str(y+1)),str("T"+chr(65+x)),tab_cost[y][x],tab_quantity_ele)
                    #print(temp.est_connexe(),temp.est_cyclique())
                    #print(temp.adj_list)
                    #print("\n \n")
                    if temp.est_connexe() and (not temp.est_cyclique()):
                        print("vrai pour ",str(chr(83)+str(y+1)),str("T"+chr(65+x)))
                        g = copy.deepcopy(temp)
                        return True
                try:
                    del temp
                except NameError:
                    pass




connexe(g)
#g.ajoute_arete('A', 'B', 1, 5)
print(g.adj_list)

print("Le graphe est cyclique:", g.est_cyclique())
print("Le graphe est connexe:", g.est_connexe())



