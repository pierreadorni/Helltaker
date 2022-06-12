#!/usr/bin/env python
# coding: utf-8
import collections


# In[1]:

def creationLaby(infos):
    map = collections.defaultdict(list)
    for i in range(infos["m"]):
        for j in range(infos["n"]):
            target = infos["grid"][i][j]
            map["board"].append((j, i))
            if target == "D":  # on ne représente pas les murs
                map["final"].append((j + 1, i))
                map["final"].append((j - 1, i))
                map["final"].append((j, i + 1))
                map["final"].append((j, i - 1))
                map["demon"].append((j, i))
            elif target == "#":
                map["wall"].append((j, i))
            elif target == "B":
                map["boxs"].append((j, i))
            elif target == "M":
                map["mob"].append((j, i))
            elif target == "H":
                map["initial"].append((j, i))
    return map





# In[2]:


def vocabulary(laby, t_max):
    directions = ("left", "right", "up", "down")
    verbs = ("move", "push")
    verb_vars = [("do_v", t, v) for t in range(t_max) for v in verbs]
    dir_vars = [("do_d", t, a) for t in range(t_max) for a in directions]
    at_vars = [("at", t, c) for t in range(t_max + 1) for c in laby["board"]]
    wall_vars = [("wall", t, c) for t in range(t_max + 1) for c in laby["board"]]
    box_vars = [("box", t, c) for t in range(t_max + 1) for c in laby["board"]]
    mob_vars = [("mob", t, c) for t in range(t_max + 1) for c in laby["board"]]
    demon_vars = [("demon", t, c) for t in range(t_max + 1) for c in laby["board"]]

    return {v: i + 1 for i, v in enumerate(verb_vars + dir_vars + at_vars + wall_vars + box_vars + mob_vars + demon_vars)}



# In[3]:


from itertools import combinations


def clauses_exactly_one_action(var2n, t_max):
    directions = ("left", "right", "up", "down")
    verbs = ("move", "push")
    at_least_one_dir = [
        [var2n[("do_d", t, a)] for a in directions] for t in range(t_max)
    ]
    at_most_one_dir = [
        [-var2n[("do_d", t, a1)], -var2n[("do_d", t, a2)]]
        for t in range(t_max)
        for a1, a2 in combinations(directions, 2)
    ]
    at_least_one_verb = [[var2n[("do_v", t, a)] for a in verbs] for t in range(t_max)]
    at_most_one_verb = [
        [-var2n[("do_v", t, a1)], -var2n[("do_v", t, a2)]]
        for t in range(t_max)
        for a1, a2 in combinations(verbs, 2)
    ]
    return at_least_one_dir + at_most_one_dir + at_least_one_verb + at_most_one_verb




# In[4]:


def clauses_initial_state(var2n, laby):
    cl = []
    for c in laby["board"]:
        if c == laby["initial"]:
            cl.append([var2n[("at", 0, c)]])
        else:
            cl.append([-var2n[("at", 0, c)]])
    for c in laby["board"]:
        if c in laby["walls"]:
            cl.append([var2n[("wall", 0, c)]])
        else:
            cl.append([-var2n[("wall", 0, c)]])
    for c in laby["board"]:
        if c in laby["boxs"]:
            cl.append([var2n[("box", 0, c)]])
        else:
            cl.append([-var2n[("box", 0, c)]])
    for c in laby["board"]:
        if c in laby["mobs"]:
            cl.append([var2n[("mob", 0, c)]])
        else:
            cl.append([-var2n[("mob", 0, c)]])
    for c in laby["board"]:
        if c in laby["demon"]:
            cl.append([var2n[("demon", 0, c)]])
        else:
            cl.append([-var2n[("demon", 0, c)]])
    return cl



# In[6]:


def succ(at, direction, board):
    x, y = at
    return {
        "left": (x - 1, y),
        "right": (x + 1, y),
        "up": (x, y - 1),
        "down": (x, y + 1),
    }[direction]


def clauses_successor_from_given_position(var2n, laby, t_max, position):
    board = laby["board"]
    directions = ("left", "right", "up", "down")
    # les murs restent immobiles
    cl = [
        [var2n[("wall", t, position)], -var2n[("wall", t + 1, position)]]
        for t in range(t_max)
    ]

    # les demons ne bougent pas
    cl = [
        [var2n[("demon", t, position)], -var2n[("demon", t + 1, position)]]
        for t in range(t_max)
    ]

    # les boîtes n'apparaissent pas
    cl += [
        [var2n[("box", t, position)], -var2n[("box", t + 1, position)]]
        for t in range(t_max)
    ]

    # les monstres n'apparaissent pas
    cl += [
        [var2n[("mob", t, position)], -var2n[("mob", t + 1, position)]]
        for t in range(t_max)
    ]

    Successors = {a: succ(position, a, board) for a in directions}

    # transitions impossibles, entre deux cases *distinctes* non voisines
    cl += [
        [-var2n[("at", t, position)], -var2n[("at", t + 1, c)]]
        for t in range(t_max)
        for c in board
        if not (c in Successors.values())
        if c != position
    ]
    # surplace impossible si on ne pousse pas
    cl += [
        [
            -var2n[("at", t, position)],
            -var2n[("at", t + 1, position)],
            var2n[("do_v", t, "push")],
        ]
        for t in range(t_max)
    ]
    # directions faisant sortir du plateau interdites
    cl += [
        [-var2n[("at", t, position)], -var2n[("do_d", t, a)]]
        for t in range(t_max)
        for a, c in Successors.items()
        if not (c in board)
    ]
    # les murs non adjacents à la position ne disparaissent pas
    cl += [
        [-var2n[("at", t, position)], -var2n[("wall", t, c)], var2n[("wall", t + 1, c)]]
        for t in range(t_max)
        for c in board
        if not (c in Successors.values())
        if c != position
    ]
    # les demons non adjacents à la position ne disparaissent pas

    cl += [
        [-var2n[("at", t, position)], -var2n[("demon", t, c)], var2n[("demon", t + 1, c)]]
        for t in range(t_max)
        for c in board
        if not (c in Successors.values())
        if c != position
    ]

    # les boites non adjacents à la position ne disparaissent pas
    cl += [
        [-var2n[("at", t, position)], -var2n[("box", t, c)], var2n[("box", t + 1, c)]]
        for t in range(t_max)
        for c in board
        if not (c in Successors.values())
        if c != position
    ]

    # les monstress non adjacents à la position ne disparaissent pas
    cl += [
        [-var2n[("at", t, position)], -var2n[("mob", t, c)], var2n[("mob", t + 1, c)]]
        for t in range(t_max)
        for c in board
        if not (c in Successors.values())
        if c != position
    ]

    # On ne déplace pas les boite que l'on ne pousse pas
    cl += [
        [
            -var2n[("box", t, position)],
            var2n[("do_v", t, "push")],
            var2n[("box", t + 1, position)],
        ]
        for t in range(t_max)
    ]
    cl += [
        [
            var2n[("box", t, position)],
            var2n[("do_v", t, "push")],
            -var2n[("box", t + 1, position)],
        ]
        for t in range(t_max)
    ]
    # On ne déplace, ni ne tue les monstres que l'on ne pousse pas
    cl += [
        [
            -var2n[("mob", t, position)],
            var2n[("do_v", t, "push")],
            var2n[("mob", t + 1, position)],
        ]
        for t in range(t_max)
    ]
    cl += [
        [
            var2n[("mob", t, position)],
            var2n[("do_v", t, "push")],
            -var2n[("mob", t + 1, position)],
        ]
        for t in range(t_max)
    ]
    # on ne change pas de position si on ne se déplace pas
    cl += [
        [
            -var2n[("at", t, position)],
            var2n[("at", t + 1, position)],
            var2n[("do_v", t, "move")],
        ]
        for t in range(t_max)
    ]
    cl += [
        [
            var2n[("at", t, position)],
            -var2n[("at", t + 1, position)],
            var2n[("do_v", t, "move")],
        ]
        for t in range(t_max)
    ]
    for a, c in Successors.items():
        if c in board:
            # action : déplacer ----------------------------------------------------------------------------------------

            # at(t,position) AND do(t,a) -> at(t+1,c)
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "move")],
                    -var2n[("do_d", t, a)],
                    var2n[("at", t + 1, c)],
                ]
                for t in range(t_max)
            ]
            # on ne fonce pas dans les murs
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "move")],
                    -var2n[("do_d", t, a)],
                    -var2n[("wall", t + 1, c)],
                ]
                for t in range(t_max)
            ]
            # on ne fonce pas dans les boites
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "move")],
                    -var2n[("do_d", t, a)],
                    -var2n[("box", t + 1, c)],
                ]
                for t in range(t_max)
            ]
            # on ne fonce pas dans les monstres
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "move")],
                    -var2n[("do_d", t, a)],
                    -var2n[("mob", t + 1, c)],
                ]
                for t in range(t_max)

            ]
            # on ne fonce pas dans les demons
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "move")],
                    -var2n[("do_d", t, a)],
                    -var2n[("demon", t + 1, c)],
                ]
                for t in range(t_max)
            ]
            # unicité de la position à l'issue de l'action
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "move")],
                    -var2n[("do_d", t, a)],
                    -var2n[("at", t + 1, c1)],
                ]
                for t in range(t_max)
                for c1 in Successors.values()
                if c1 != c and c1 in board
            ]

            # action : Pousser -----------------------------------------------------------------------------------------

            # on pousse face à une boite
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "push")],
                    -var2n[("do_d", t, a)],
                    var2n[("box", t, c)],
                ]
                for t in range(t_max)
            ]
            # la boite poussée se déplace
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "push")],
                    -var2n[("do_d", t, a)],
                    var2n[("box", t + 1, c1)],
                ]
                for t in range(t_max)
                for c1 in Successors.values()
                if c1 != c and c1 in board
            ]
            # les autres boites adjacents subsistent
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_d", t, a)],
                    -var2n[("box", t, c1)],
                    var2n[("box", t + 1, c1)],
                ]
                for t in range(t_max)
                for c1 in Successors.values()
                if c1 != c and c1 in board
            ]

            # on fait face à un monstre
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "push")],
                    -var2n[("do_d", t, a)],
                    var2n[("mob", t, c)],
                ]
                for t in range(t_max)
            ]
            # le monstre poussé se déplace (si c1 succ non mur)
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "push")],
                    -var2n[("do_d", t, a)],
                    var2n[("wall", t, c1)],
                    var2n[("mob", t + 1, c1)],
                ]
                for t in range(t_max)
                for c1 in Successors.values()
                if c1 != c and c1 in board
            ]
            # le monstre poussé dans un mur meurt
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_v", t, "push")],
                    -var2n[("do_d", t, a)],
                    -var2n[("wall", t, c1)],
                    -var2n[("mob", t + 1, c)],
                ]
                for t in range(t_max)
                for c1 in Successors.values()
                if c1 != c and c1 in board
            ]
            # les autres monstres subsistent
            cl += [
                [
                    -var2n[("at", t, position)],
                    -var2n[("do_d", t, a)],
                    -var2n[("mob", t, c1)],
                    var2n[("mob", t + 1, c1)],
                ]
                for t in range(t_max)
                for c1 in Successors.values()
                if c1 != c and c1 in board
            ]
    return cl




# In[7]:


def sat_laby2(laby, t_max):
    var2n = vocabulary(laby, t_max)
    clauses = clauses_exactly_one_action(var2n, t_max) + clauses_initial_state(
        var2n, laby
    )
    for c in laby["board"]:
        clauses += clauses_successor_from_given_position(var2n, laby, t_max, c)

    if type(laby["final"]) == list:
        for c in laby["final"]:
            clauses.append([var2n[("at", t_max, c)]])
    else:
        clauses.append([var2n[("at", t_max, laby["final"])]])

    return var2n, clauses



# In[9]:


import subprocess


def clauses_to_dimacs(clauses, numvar):
    dimacs = "c This is it\np cnf " + str(numvar) + " " + str(len(clauses)) + "\n"
    for clause in clauses:
        for atom in clause:
            dimacs += str(atom) + " "
        dimacs += "0\n"
    return dimacs


def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(filename: str, cmd: str = "gophersat", encoding: str = "utf8"):
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:].split(" ")

    return True, [int(x) for x in model]


# In[10]:


def solve_laby2(infos):
    t_max = infos["max_steps"]
    laby = creationLaby(infos)
    print(laby)

    for t in range(1, t_max):
        v2n, cl = sat_laby2(laby, t)
        n2v = {i: v for v, i in v2n.items()}
        dimacs = clauses_to_dimacs(cl, len(v2n))
        filename = f"laby2_{t!s}.cnf"
        write_dimacs_file(dimacs, filename)
        sat, model = exec_gophersat(filename)
        if sat:
            print( [n2v[i] for i in model if i > 0 and n2v[i][0] in ("do_d", "do_v")])
        else:
            print("pas de plan de taille", t)



# In[ ]:


# In[ ]:
