class Graphe:
    def __init__(self):
        self.adj_list = {}
        self.cost_tab=[]

    def ajoute_arete(self, src, dest, cout, quantite):
        if src not in self.adj_list:
            self.adj_list[src] = []
        if dest not in self.adj_list:
            self.adj_list[dest] = []
        self.adj_list[src].append((dest, cout, quantite))

    def est_cyclique(self):
        visited = set()
        rec_stack = set()

        def visite(noeud):
            if noeud in rec_stack:
                return True
            if noeud in visited:
                return False
            visited.add(noeud)
            rec_stack.add(noeud)
            for voisin, _, _ in self.adj_list.get(noeud, []):
                if visite(voisin):
                    return True
            rec_stack.remove(noeud)
            return False

        for n in self.adj_list:
            if visite(n):
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



# Utilisation de la classe Graphe
g = Graphe()
"""
g.ajoute_arete('S1', 'TB', 1, 2000)
g.ajoute_arete('S2', 'TB', 2, 1000)
g.ajoute_arete('S2', 'TC', 2, 2000)
g.ajoute_arete('S2', 'TD', 0, 3000)
g.ajoute_arete('S3', 'TA', 1, 5000)
g.ajoute_arete('S3', 'TD', 0, 1000)
g.ajoute_arete('S3', 'TC', 1, 1000)
g.ajoute_arete('S1', 'TA', 1, 1000)
"""

g.ajoute_arete('S1', 'TA', 5, 2000)
g.ajoute_arete('S2', 'TA', 6, 1000)
g.ajoute_arete('S2', 'TB', 8, 2000)
g.ajoute_arete('S3', 'TB', 7, 3000)
g.ajoute_arete('S3', 'TC', 7, 5000)
g.cost_tab= [[5,7,8],[6,8,5],[6,7,7]]

"""
g.ajoute_arete('S1', 'TA', 7, 2000)
g.ajoute_arete('S1', 'TB', 12, 2000)
g.ajoute_arete('S2', 'TB', 3, 1000)
g.ajoute_arete('S2', 'TC', 12, 1000)
g.ajoute_arete('S3', 'TC', 10, 1000)
g.ajoute_arete('S3', 'TD', 12, 1000)
g.ajoute_arete('S4', 'TD', 11, 1000)
g.ajoute_arete('S4', 'TE', 16, 1000)
"""

a=g.potentiels()
print(a)
matrix=g.potential_cost_matrix(a)
matrix2 =g.marginal_cost_matrix(matrix)
print(matrix2)

print("Le graphe est cyclique:", g.est_cyclique())
print("Le graphe est connexe:", g.est_connexe())