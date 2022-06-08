from itertools import combinations
import collections


def successeur(Cases, action, case):
    if action == "haut" and (case[0], case[1] + 1) in Cases:
        return [(case[0], case[1] + 1)]
    elif action == "bas" and (case[0], case[1] - 1) in Cases:
        return [(case[0], case[1] - 1)]
    elif action == "gauche" and (case[0] - 1, case[1]) in Cases:
        return [(case[0] - 1, case[1])]
    elif action == "droite" and (case[0] + 1, case[1]) in Cases:
        return [(case[0] + 1, case[1])]
    return []


def voisin(Cases, cible):
    for x in Cases:
        if x in [
            [cible[0] + 1, cible[1]],
            [cible[0] - 1, cible[1]],
            [cible[0], cible[1] + 1],
            [cible[0], cible[1] - 1],
        ]:
            return True
    return False


def creation_cnf(clauses):
    text = "c === Helltaker SAT solver === \n"
    text += "c\n"
    text += f"p cnf {len(clauses[0])} {len(clauses[1])} \n"
    for clause in clauses[0]:
        if type(clause) == list:
            for var in clause:
                text += f"{var} "
            text += "0 \n"
        else:
            text += f"{clause} 0 \n"

    return text


def get_target(action):
    if action in ["attaquerHaut", "attaquerBas", "attaquerGauche", "attaquerDroite"]:
        return "M"
    elif action in ["pousserHaut", "pousserBas", "pousserGauche", "pousserDroite"]:
        return "B"
    return None


def create_map(infos):  # map est un dict contenant les coordonnées des obstacles
    map = collections.defaultdict(list)
    for i in range(infos["m"]):
        for j in range(infos["n"]):
            target = infos["grid"][i][j]
            if target != "#":  # on ne représente pas les murs
                map[target].append((i, j))
    return map


def create_Cases(map):  # on crée une liste de tous les emplacements occupables
    Cases = []
    for key in map.keys():
        for case in map[key]:
            Cases.append(case)
    return Cases


def deplacer_personnage_Haut(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "haut")],
            var2n[("at", t, c1, "H")],
            var2n[("at", t + 1, c2, "H")],
            var2n[("at", t, c2, " ")],
        ]
        for t in range(t_max)
        for c1 in Cases
        for c2 in successeur(Cases, "haut", c1)
    ]
    return contrainte


def deplacer_personnage_Bas(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "bas")],
            var2n[("at", t, c1, "B")],
            var2n[("at", t + 1, c2, "B")],
            var2n[("at", t, c2, " ")],
        ]
        for t in range(t_max)
        for c1 in Cases
        for c2 in successeur(Cases, "bas", c1)
    ]
    return contrainte


def deplacer_personnage_Gauche(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "gauche")],
            var2n[("at", t, c1, "H")],
            var2n[("at", t + 1, c2, "H")],
            var2n[("at", t, c2, " ")],
        ]
        for t in range(t_max)
        for c1 in Cases
        for c2 in successeur(Cases, "gauche", c1)
    ]
    return contrainte


def deplacer_personnage_Droite(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "droite")],
            var2n[("at", t, c1, "D")],
            var2n[("at", t + 1, c2, "D")],
            var2n[("at", t, c2, " ")],
        ]
        for t in range(t_max)
        for c1 in Cases
        for c2 in successeur(Cases, "droite", c1)
    ]
    return contrainte


def deplacer_pierre_Haut(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "pousserHaut")],
            var2n[("at", t, c1, "H")],
            var2n[("at", t + 1, c1, "H")],
            var2n[("at", t, (c1[0], c1[1] + 1), "B")],
            var2n[("at", t + 1, (c1[0], c1[1] + 1), " ")],
            var2n[("at", t + 1, (c1[0], c1[1] + 2), "B")],
        ]
        for t in range(t_max)
        for c1 in Cases
        if (c1[0], c1[1] + 1) in Cases
        if (c1[0], c1[1] + 2) in Cases
    ]
    return contrainte


def deplacer_pierre_Bas(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "pousserBas")],
            var2n[("at", t, c1, "B")],
            var2n[("at", t, (c1[0], c1[1] - 1), "H")],
            var2n[("at", t + 1, (c1[0], c1[1] - 1), " ")],
            var2n[("at", t + 1, (c1[0], c1[1] - 2), "H")],
        ]
        for t in range(t_max)
        for c1 in Cases
        if (c1[0], c1[1] - 2) in Cases
        if (c1[0], c1[1] - 1) in Cases
    ]
    return contrainte


def deplacer_ennemi_Haut(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "attaquerHaut")],
            var2n[("at", t, c1, "H")],
            var2n[("at", t, (c1[0], c1[1] + 1), "M")],
            var2n[("at", t, (c1[0], c1[1] + 2), " ")],
            var2n[("at", t + 1, (c1[0], c1[1] + 2), "M")],
        ]
        for t in range(t_max)
        for c1 in Cases
        if (c1[0], c1[1] + 2) in Cases
        if (c1[0], c1[1] + 1) in Cases
    ]
    return contrainte


def eliminer_ennemi_Haut(t_max, Cases, var2n):
    contrainte = [
        [
            var2n[("do", t, "tuerHaut")],
            var2n[("at", t, c1, "H")],
            var2n[("at", t, (c1[0], c1[1] + 1), "M")],
        ]
        for t in range(t_max)
        for c1 in Cases
        if (c1[0], c1[1] + 1) in Cases
    ]
    return contrainte


def nouvelle_map(map, t_max, Actions, Cases, var2n):
    nouvelle_map = [
        [
            var2n[("at", t, c, entite)],
            var2n[("at", t + 1, c, entite)],
            var2n[("do", t, action)],
        ]
        for t in range(t_max)
        for c in Cases
        for entite in map.keys()
        for action in Actions
        if entite != get_target(action)
    ]

    # on fait réapparaître les entités avec un rapport avec
    # l'action, mais qui n'en sont pas la cible (par ex les mobs non ciblés)
    nouvelle_map += [
        [
            var2n[("at", t, c, entite)],
            var2n[("at", t + 1, c, entite)],
            var2n[("do", t, action)],
        ]
        for t in range(t_max)
        for c in Cases
        for entite in map.keys()
        for action in Actions
        if entite == get_target(action)
        if action
        not in [
            "pousserHaut",
            "pousserBas",
            "pousserGauche",
            "pousserDroite",
            "attaquerHaut",
            "attaquerBas",
            "attaquerGauche",
            "attaquerDroite",
        ]
    ]
    return nouvelle_map


def objectif(t_max, Cases, var2n):
    objectif = [
        [var2n[("at", t, c1, "H")], var2n[("at", t, c2, "D")]]
        for t in range(t_max)
        for c2 in Cases
        for c1 in [
            (c2[0] + 1, c2[1]),
            (c2[0] - 1, c2[1]),
            (c2[0], c2[1] + 1),
            (c2[0], c2[1] - 1),
        ]
        if c1 in Cases
    ]
    return objectif


def sat_solver(infos):
    # a voir si on fusionne attaquerHaut et pousserHaut
    Actions = (
        "haut",
        "bas",
        "gauche",
        "droite",
        "attaquerHaut",
        "attaquerBas",
        "attaquerGauche",
        "attaquerDroite",
        "tuerHaut",
        "tuerBas",
        "tuerGauche",
        "tuerDroite",
        "pousserHaut",
        "pousserBas",
        "pousserGauche",
        "pousserDroite",
    )
    t_max = infos["max_steps"]
    map = create_map(infos)
    Cases = create_Cases(map)
    do_vars = [("do", t, a) for t in range(t_max) for a in Actions]
    at_vars = [
        ("at", t, c, entite)
        for t in range(t_max + 1)
        for c in Cases
        for entite in map.keys()
    ]

    var2n = {v: i + 1 for i, v in enumerate(do_vars + at_vars)}
    n2var = {n: v for v, n in var2n.items()}

    at_least_one_action = [[var2n[("do", t, a)] for a in Actions] for t in range(t_max)]
    at_most_one_action = [
        [-var2n[("do", t, a1)], -var2n[("do", t, a2)]]
        for a1, a2 in combinations(Actions, 2)
        for t in range(t_max)
    ]

    # on crée les clauses logique des positions de départ
    mapdepart = [
        var2n[("at", 0, case, entite)] for entite in map.keys() for case in map[entite]
    ]

    # goal
    # a voir si on ne fait que pour t = Tmax
    goal = objectif(t_max, Cases, var2n)

    # a modifier quand on rajoute les piques car var2n[('at', t, c2, " ")] bloque le deplacement
    deplacement_personnage_Haut = deplacer_personnage_Haut(t_max, Cases, var2n)
    deplacement_personnage_Bas = deplacer_personnage_Bas(t_max, Cases, var2n)
    deplacement_personnage_Gauche = deplacer_personnage_Gauche(t_max, Cases, var2n)
    deplacement_personnage_Droite = deplacer_personnage_Droite(t_max, Cases, var2n)

    deplacement_pierre_Haut = deplacer_pierre_Haut(t_max, Cases, var2n)
    deplacement_pierre_Bas = deplacer_pierre_Bas(t_max, Cases, var2n)

    deplacement_ennemi_haut = deplacer_ennemi_Haut(t_max, Cases, var2n)

    elimination_ennemi_haut = eliminer_ennemi_Haut(t_max, Cases, var2n)

    # mise a jour de la carte pour les element inchangés à un nouveau t
    # on fait reappaaraitre en t+1 toutes les entités sans rapport avec l'action
    nouvelle_carte = nouvelle_map(map, t_max, Actions, Cases, var2n)

    Clauses = (
        mapdepart
        + at_least_one_action
        + at_most_one_action
        + deplacement_personnage_Haut
        + deplacement_personnage_Bas
        + deplacement_personnage_Gauche
        + deplacement_personnage_Droite
        + deplacement_pierre_Haut
        + deplacement_pierre_Bas
        + deplacement_ennemi_haut
        + elimination_ennemi_haut
        + nouvelle_carte
        + goal
    )

    return [Clauses, var2n, n2var]


def lecture_solus(file):
    with open(file, "r") as f:
        line = f.readlines()[2]
    solus = []
    clause = ""
    for char in range(len(line)):
        if line[char].isdigit():
            if line[char - 1] == " ":
                while line[char].isdigit():
                    clause += line[char]
                    char += 1
                solus.append(clause)
                clause = ""
    solus.pop()
    return solus


def solus_clause(clauses, solution):
    clause_vraie = []
    liste_clauses = lecture_solus(solution)
    for i in range(len(liste_clauses)):
        with open(clauses, "r") as f:
            line = f.readlines()[i + 3]
            clause_vraie.append(line)
    return clause_vraie


def exam(clauses, solution, n2var):
    solus = solus_clause(clauses, solution)
    clause = ""
    actions = []
    for i in range(len(solus)):
        for char in range(len(solus[i])):
            if solus[i][char].isdigit() and solus[i][char] != "0":
                if solus[i][char - 1] == " ":
                    while solus[i][char].isdigit():
                        clause += solus[i][char]
                        char += 1
                    actions.append(int(clause))
                    clause = ""
    return solutionner(actions, n2var)


def solutionner(actions, n2var):
    solution = []
    for i in range(len(actions)):
        solution.append(n2var[actions[i]])
    print(solution)
    return solution
