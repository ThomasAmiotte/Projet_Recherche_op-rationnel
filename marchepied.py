import copy
class Graphe:
    def __init__(self):
        self.adj_list = {}

    def init(self, tab_quantity):
        for y, ligne in enumerate(tab_quantity):
            for x, tab_quantity_ele in enumerate(ligne):
                if tab_quantity_ele:
                    self.ajoute_arete(str(chr(83) + str(y + 1)), str("T" + chr(65 + x)), tab_cost[y][x], tab_quantity_ele)

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

    def potentiels(self):
        def potential_calculation(current_node_key):
            if str(current_node_key)[0]=='S':
                for arete in self.adj_list[current_node_key]:
                    if arete[0] not in potential_dic.keys():
                        potential_dic[arete[0]]= potential_dic[current_node_key]-arete[1]
                        potential_calculation(arete[0])
            else:
                for nodekey,aretes in self.adj_list.items():
                    for arete in aretes:
                        if arete[0]==current_node_key:
                            potential_dic[nodekey] = potential_dic[current_node_key] + arete[1]
                            potential_calculation(nodekey)

        potential_dic= {}
        if not self.adj_list or len(self.adj_list)<2:
            return potential_dic

        max_links=0
        key_initialisation=None
        for key in self.adj_list.keys():
            if len(self.adj_list[key])>max_links:
                max_links= len(self.adj_list[key])
                key_initialisation=key
        potential_dic[key_initialisation]=0

        potential_calculation(key_initialisation)
        return potential_dic

    def potential_cost_matrix(self,potential_dic):
        matrix = []
        n=0
        m=0
        for i in potential_dic.keys():
            if str(i[0])=='S':
                n+=1
            elif str(i[0])=='T':
                m+=1
        print(n, m)
        for i in range(n):
            matrix.append([None]*m)
            for j in range(m):
                matrix[i][j]= potential_dic['S'+str(i+1)]-potential_dic['T'+chr(ord('A')+j)]

        return matrix

    def marginal_cost_matrix(self,potential_cost_matrix):
        marginal_matrix=[]
        for i in range(len(potential_cost_matrix)):
            marginal_matrix.append([None]*len(potential_cost_matrix[0]))
            for j in range(len(potential_cost_matrix[0])):
                marginal_matrix[i][j] = self.cost_tab[i][j] - potential_cost_matrix[i][j]
        return marginal_matrix

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
                        print("Ajout de l'arête: ",str(chr(83)+str(y+1)),str("T"+chr(65+x)))
                        g = copy.deepcopy(temp)
                        return g
                try:
                    del temp
                except NameError:
                    pass



tab_cost = [[10,5,5,3],[10,4,5,5],[4,4,3,5]]
tab_quantity = [[6,0,6,0],[0,12,0,0],[0,0,3,9]]
g = Graphe()
g.init(tab_quantity)






