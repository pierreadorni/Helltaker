from itertools import combinations
import collections


def successeur(Cases, action, case):
    if action == "bas" and (case[0], case[1] + 1) in Cases:
            return ((case[0], case[1] + 1))
    elif action == "haut" and (case[0], case[1] - 1) in Cases:
        return ((case[0], case[1] - 1))
    elif action == "gauche" and (case[0] - 1, case[1]) in Cases:
        return ((case[0] - 1, case[1]))
    elif action == "droite" and (case[0] + 1, case[1]) in Cases:
        return ((case[0] + 1, case[1]))
    return []


def get_value(cible, n2var):
    if cible in n2var:
        return n2var[cible]
    else:
        return 0


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
    text += f"p cnf {len(clauses[1])} {len(clauses[0])} \n"
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


def get_actions(target):
    liste_target =["haut", "bas", "gauche", "droite"]
    if "M" in target:
        liste_target += ["attaquerHaut", "attaquerBas", "attaquerGauche", "attaquerDroite", "tuerHaut", "tuerBas", "tuerGauche", "tuerDroite"]
    if "B" in liste_target:
        liste_target+= ["pousserHaut", "pousserBas", "pousserGauche", "pousserDroite"]
    return liste_target


def create_map(infos):  # map est un dict contenant les coordonnées des obstacles
    map = collections.defaultdict(list)
    for i in range(infos["m"]):
        for j in range(infos["n"]):
            target = infos["grid"][i][j]
            if target != "#":  # on ne représente pas les murs
                map[target].append((j, i))
    return map


def create_Cases(map):  # on crée une liste de tous les emplacements occupables
    Cases = []
    for key in map.keys():
        for case in map[key]:
            Cases.append(case)
    return Cases


def deplacer_personnage(t_max,Cases,var2n):
    contrainte = [
        [
            var2n[("do", t, direction)],
            var2n[("at", t, c1, "H")],
            var2n[("at", t, c2, " ")],
            var2n[("at", t + 1, c2, "H")],
            var2n[("at", t + 1, c1, " ")]
        ]
        for t in range(t_max)
        for c1,c2 in combinations(Cases,2)
        for direction in ["haut", "bas", "gauche", "droite"]
        if c2 == successeur(Cases, direction, c1)
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


def nouvelle_map(t_max, Actions, Cases, var2n, position_demon):

    # si le hero ne bouge pas, il bouge pas
    hero = [
        [
            var2n[('at', t, c, "H")],
            -var2n[('do', t, "haut")],
            -var2n[('do', t, "bas")],
            -var2n[('do', t, "gauche")],
            -var2n[('do', t, "droite")],
            var2n[('at', t + 1, c, "H")]
        ]
        for t in range(t_max)
        for c in Cases
    ]

<<<<<<< HEAD
    # on fait réapparaître les entités avec un rapport avec
    # l'action, mais qui n'en sont pas la cible (par ex les mobs non ciblés)
    nouvelle_map += [
=======
    # le hero est dans une seule case a la fois
    hero += [
>>>>>>> 657ce39 (nouveau code SatSolever2.py)
        [
            var2n[('at', t, c1, "H")],
            -var2n[('at', t, c2, "H")]
        ]
        for t in range(1,t_max)
        for c1, c2 in combinations(Cases, 2)
    ]



    # la demonne ne bouge pas
    demon = [
        [
            var2n[("at", t, position_demon, "D")]
        ]
        for t in range(t_max)
    ]

# si le hero ne va pas dans une case vide, elle reste vide
    case_simple = [
        [
            var2n[("do",t,direction)],
            var2n[("at", t, c2, "H")],
            var2n[("at", t, c1, " ")],
            var2n[('at', t + 1, c1, " ")]
        ]
        for direction in ["haut", "bas", "gauche", "droite"]
        for t in range(t_max)
        for c1 in Cases
        for c2 in Cases
        if c1 != successeur(Cases, direction, c2)
        ]

    nouvelle_map = hero + case_simple + demon

    return nouvelle_map


def objectif(t_max, Cases, var2n, position_demon):
    objectif = [
        [var2n[("at", t, c1, "H")], var2n[("at", t, position_demon, "D")]]
        for t in range(t_max)
        for c1 in [
            (position_demon[0] + 1, position_demon[1]),
            (position_demon[0] - 1, position_demon[1]),
            (position_demon[0], position_demon[1] + 1),
            (position_demon[0], position_demon[1] - 1),
        ]
        if c1 in Cases
    ]
    return objectif


def sat_solver(infos):
    t_max = infos["max_steps"]
    map = create_map(infos)

    Actions = get_actions(map.keys())

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
        for t in range(t_max)
        for a1, a2 in combinations(Actions, 2)
    ]

    # on crée les clauses logique des positions de départ
    mapdepart = [
        var2n[("at", 0, case, entite)] for entite in map.keys() for case in map[entite]
    ]
    # goal
    # a voir si on ne fait que pour t = Tmax

    #on recupére la position du demon
    for x in mapdepart:
        if n2var[x][3] == "D":
            position_demon = n2var[x][2]

    goal = objectif(t_max, Cases, var2n,position_demon)

    # a modifier quand on rajoute les piques car var2n[('at', t, c2, " ")] bloque le deplacement
    deplacement_personnage = deplacer_personnage(t_max, Cases, var2n)


    # mise a jour de la carte pour les element inchangés à un nouveau t
    # on fait reappaaraitre en t+1 toutes les entités sans rapport avec l'action


    nouvelle_carte = nouvelle_map(t_max, Actions, Cases, var2n, position_demon)

    Clauses = (
            mapdepart
            + at_least_one_action
            + at_most_one_action
            + deplacement_personnage
            + nouvelle_carte
            + goal
    )
    print(Cases)

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


def solutionner(solution, n2var):
    actions = lecture_solus(solution)
    solution = []
    for i in range(len(actions)):
        solution.append(n2var[int(actions[i])])
    print(solution)
    return solution
