#!/usr/bin/env python
# coding: utf-8
import collections

def creationLaby(infos):
    map = collections.defaultdict(list)
    for i in range(infos["m"]):
        for j in range(infos["n"]):
            target = infos["grid"][i][j]
            if target == "#":
                map["wall"].append((j, i))
            else:
                map["board"].append((j, i))
                if target == "D":
                    map["demon"].append((j, i))
                elif target == "B":
                    map["block"].append((j, i))
                elif target == "M":
                    map["mob"].append((j, i))
                elif target == "H":
                    map["initial"].append((j, i))

    #ajout des etats finaux
    for coord in map["demon"]:
        if (coord[0] + 1, coord[1]) not in map["wall"]:
            map["final"].append((coord[0] + 1, coord[1]))
        if (coord[0] - 1, coord[1]) not in map["wall"]:
            map["final"].append((coord[0] - 1, coord[1]))
        if (coord[0], coord[1] + 1) not in map["wall"]:
            map["final"].append((coord[0], coord[1] + 1))
        if (coord[0], coord[1] - 1) not in map["wall"]:
            map["final"].append((coord[0], coord[1] - 1))
    return map

def vocabulary(laby, t_max):
    directions = ("left", "right", "up", "down")
    verbs = ("move", "push")
    verb_vars = [("do_v", t, v) for t in range(t_max) for v in verbs]
    dir_vars = [("do_d", t, a) for t in range(t_max) for a in directions]
    at_vars = [("at", t, c) for t in range(t_max + 1) for c in laby["board"]]
    wall_vars = [("wall", t, c) for t in range(t_max + 1) for c in laby["wall"]]
    block_vars = [("block", t, c) for t in range(t_max + 1) for c in laby["board"]]
    demon_vars = [("demon", t, c) for t in range(t_max + 1) for c in laby["board"]]

    return {
        v: i + 1
        for i, v in enumerate(
            verb_vars
            + dir_vars
            + at_vars
            + wall_vars
            + block_vars
            + demon_vars
        )
    }

from itertools import combinations


def clauses_exactly_one_action(var2n, t_max) :
    directions = ('left','right','up','down')
    verbs = ('move', 'push')
    at_least_one_dir = [[var2n[('do_d',t,a)] for a in directions] for t in range(t_max)]
    at_most_one_dir  = [[-var2n[('do_d',t,a1)], -var2n[('do_d',t,a2)]]
                          for t in range(t_max) for a1,a2 in combinations(directions, 2)]
    at_least_one_verb = [[var2n[('do_v',t,a)] for a in verbs] for t in range(t_max)]
    at_most_one_verb  = [[-var2n[('do_v',t,a1)], -var2n[('do_v',t,a2)]]
                          for t in range(t_max) for a1,a2 in combinations(verbs, 2)]
    return at_least_one_dir + at_most_one_dir + at_least_one_verb + at_most_one_verb

def clauses_initial_state(var2n, laby):
    cl = []
    for c in laby["board"]:
        if c in laby["initial"]:
            cl.append([var2n[("at", 0, c)]])
        else:
            cl.append([-var2n[("at", 0, c)]])
    for c in laby["board"]:
        if c in laby["block"]:
            cl.append([var2n[("block", 0, c)]])
        else:
            cl.append([-var2n[("block", 0, c)]])
    for c in laby["board"]:
        if c in laby["demon"]:
            cl.append([var2n[("demon", 0, c)]])
        else:
            cl.append([-var2n[("demon", 0, c)]])
    return cl

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

    # les demons ne bougent pas
    cl = [
        [
            -var2n[("demon", t, position)],
            var2n[("demon", t + 1, position)],
        ]
        for t in range(t_max)
    ]





    Successors = {a: succ(position, a, board) for a in directions}
    # transitions impossibles, entre deux cases *distinctes* non voisines
    cl += [[-var2n[('at', t, position)], -var2n[('at', t + 1, c)]]
           for t in range(t_max) for c in board if not (c in Successors.values()) if c != position]

    # surplace impossible si on ne push pas
    cl += [[-var2n[('at', t, position)], -var2n[('at', t + 1, position)],var2n[('do_v', t, 'push')]]
           for t in range(t_max)]

    # directions faisant sortir du plateau interdites
    cl += [[-var2n[('at', t, position)], -var2n[('do_d', t, a)]]
           for t in range(t_max) for a, c in Successors.items() if not (c in board)]

    # les block non adjacents à la position ne disparaissent pas
    cl += [[-var2n[('at', t, position)], -var2n[('block', t, c)], var2n[('block', t + 1, c)]]
           for t in range(t_max) for c in board if not (c in Successors.values()) if c != position]

    # On ne détruit pas de block si on ne push pas
    # not(push(t)) AND block(t,position) -> block(t+1,position)
    cl += [[-var2n[('block', t, position)], var2n[('do_v', t, 'push')], var2n[('block', t + 1, position)]] for t in
              range(t_max)]

    # on ne change pas de position si on ne se déplace pas
    cl += [[-var2n[('at', t, position)], var2n[('at', t + 1, position)], var2n[('do_v', t, 'move')]]
           for t in range(t_max)]

    for a, c in Successors.items():
        if c in board:
            # action de déplacement
            # at(t,position) AND do(t,a) -> at(t+1,c)
            cl += [[-var2n[('at', t, position)], -var2n[('do_v', t, 'move')], -var2n[('do_d', t, a)],
                    var2n[('at', t + 1, c)]]
                   for t in range(t_max)]

            # on ne fonce pas dans les blocks
            cl += [[-var2n[('at', t, position)], -var2n[('do_v', t, 'move')], -var2n[('do_d', t, a)],
                    -var2n[('block', t + 1, c)]]
                   for t in range(t_max)]

            # unicité de la position à l'issue de l'action
            cl += [[-var2n[('at', t, position)], -var2n[('do_v', t, 'move')], -var2n[('do_d', t, a)],
                    -var2n[('at', t + 1, c1)]]
                   for t in range(t_max) for c1 in Successors.values() if c1 != c and c1 in board]


            # action : Push -----------------------------------------------------------------------------------------
            # on push face à un block
            cl += [
                [-var2n[('at', t, position)], -var2n[('do_v', t, 'push')], -var2n[('do_d', t, a)], var2n[('block', t, c)]]
                for t in range(t_max)]

            # le block poussé disparait de sa position d'origine
            cl += [[-var2n[('at', t, position)], -var2n[('do_v', t, 'push')], -var2n[('do_d', t, a)],
                    -var2n[('block', t + 1, c)]]
                     for t in range(t_max)]
            # deplacement du mur
            # mur(t,position) AND do(t,a) -> mur(t+1,c)
            cl += [[-var2n[('block', t, position)], -var2n[('do_v', t, 'push')], -var2n[('do_d', t, a)],
                    var2n[('block', t + 1, c)]]
                   for t in range(t_max)]

            # le block ne va pas dans les blocks
            cl += [[-var2n[('block', t, position)], -var2n[('do_v', t, 'move')], -var2n[('do_d', t, a)],
                    -var2n[('block', t + 1, c)]]
                   for t in range(t_max)]



            # le block ne va pas dans les demons
            cl += [[-var2n[('block', t, position)], -var2n[('do_v', t, 'move')], -var2n[('do_d', t, a)],
                    -var2n[('demon', t + 1, c)]]
                   for t in range(t_max)]

            # les autres blocks adjacents subsistent
            cl += [[-var2n[('at', t, position)], -var2n[('do_d', t, a)], -var2n[('block', t, c1)],
                    var2n[('block', t + 1, c1)]]
                     for t in range(t_max) for c1 in Successors.values() if c1 != c and c1 in board]
    return cl

def sat_laby2(laby, t_max):
    var2n = vocabulary(laby, t_max)
    clauses = clauses_exactly_one_action(var2n, t_max) + clauses_initial_state(
        var2n, laby
    )

    for c in laby["board"]:
        clauses += clauses_successor_from_given_position(var2n, laby, t_max, c)

    if type(laby["final"]) == list:
        x = laby["final"]
        for c in laby["final"]:

            final_states = [x for x in laby["final"] if x != c]
            Tclauses = [var2n[("at", t_max, c)]]
            for state in final_states:
                Tclauses += [-var2n[("at", t_max, state)]]
            clauses += [Tclauses]
    else:
        clauses.append([var2n[("at", t_max, laby["final"])]])

    return var2n, clauses

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

def solve_laby2(infos):
    t_max1 = infos["max_steps"] + 1
    laby = creationLaby(infos)
    for t_max in range(t_max1):
        v2n, cl = sat_laby2(laby, t_max)
        n2v = {i: v for v, i in v2n.items()}
        dimacs = clauses_to_dimacs(cl, len(v2n))
        filename = f"laby2_{t_max!s}.cnf"
        write_dimacs_file(dimacs, filename)
        sat, model = exec_gophersat(filename)
        if sat:
            print([n2v[i] for i in model if i > 0 and n2v[i][0] in ['block']])
        else:
            print("pas de plan de taille", t_max)