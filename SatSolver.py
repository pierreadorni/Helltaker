from itertools import combinations
from utils import grid_from_file
import collections

def successeur(Cases, action, case):
    if action == "haut" and (case[0], case[1]+1) in Cases:
        return [(case[0], case[1]+1)]
    return []


def sat_solver(infos):
    deplacementSimple = ("haut", "bas", "gauche", "droite")
    Actions = ("haut", "bas", "gauche", "droite",
               "attaquerHaut", "attaquerBas", "attaquerGauche", "attaquerDroite",
               "tuerHaut", "tuerBas", "tuerGauche", "tuerDroite",
               "pousserHaut", "pousserBas", "pousserGauche", "pousserDroite")
    map = collections.defaultdict(list)

    t_max = infos["max_steps"]
    # map est un dict contenant les coordonnées des obstacles
    for i in range(infos["m"]):
        for j in range(infos["n"]):
            target = infos["grid"][i][j]
            if target != "#":  # on ne représente pas les murs
                map[target].append((i, j))

    # on crée une liste de tous les emplacements occupables
    Cases = []
    for x in map:
        for y in map[x]:
            Cases.append(y)

    do_vars = [('do', t, a) for t in range(t_max) for a in Actions]
    at_vars = [('at', t, c, entite) for t in range(t_max + 1)
               for c in Cases for entite in map.keys()]

    var2n = {v: i + 1 for i, v in enumerate(do_vars + at_vars)}

    at_least_one_action = [[var2n[('do', t, a)] for a in Actions] for t in range(t_max)]
    at_most_one_action = [[-var2n[('do', t, a1)], -var2n[('do', t, a2)]]
                          for a1, a2 in combinations(Actions, 2) for t in range(t_max)]
    #on crée les clauses logique des positions de départ

    mapdepart = []
    for entite in map.keys():
        for case in map[entite]:
            mapdepart.append(var2n[('at', 0, case, entite)])

    # goal


    # deplacement du hero vers le haut
    # a modifier quand on rajoute les piques car var2n[('at', t, c2, " ")] bloque le deplacement
    deplacement_personnage_Haut = [[var2n[('do', t, "haut")], var2n[('at', t, c1, "H")], var2n[('at', t + 1, c2, "H")],
                                    var2n[('at', t, c2, " ")]]
                                   for t in range(t_max)
                                   for c1 in Cases
                                   for c2 in successeur(Cases, "haut", c1)
                                   ]


    # quand le hero pousse une pierre en haut
    deplacement_pierre_haut = [[var2n[('do', t, "pousserHaut")], var2n[('at', t, c1, "H")], var2n[('at', t, (c1[0], c1[1]+1), "B")], var2n[('at', t + 1, (c1[0], c1[1]+2), " ")],
                           var2n[('at', t+1, (c1[0], c1[1]+2), "B")]]
                                   for t in range(t_max)
                                   for c1 in Cases
                          if (c1[0], c1[1]+2) in Cases
                          if (c1[0], c1[1]+1) in Cases
                                   ]



    #
    Clauses = mapdepart + at_least_one_action + at_most_one_action + deplacement_personnage_Haut + deplacement_pierre_haut


filename = r"D:\Alex\Etude\Superieur\UTC\Informatique\IA02\Projet\helltaker_ia02\levels\level1.txt"
# récupération de la grille et de toutes les infos
infos = grid_from_file(filename)
sat_solver(infos)
