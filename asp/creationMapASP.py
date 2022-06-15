import subprocess
from operator import itemgetter


def exec_asp(filename: str, cmd: str = "clingo", encoding: str = "utf8"):
    result = subprocess.run(
        ["clingo", "solver_asp.lp"], capture_output=True
    ).stdout.decode("utf-8")
    chemin = result.split("\n")[4]
    return formater_chemin(chemin)


def formater_chemin(chemin: str):
    chemin = chemin.split(" ")
    if chemin == [""]:
        return "Unsatisfiable"
    actions = []
    plan = ""
    for action in chemin:
        target = action[3 : action.find(",")]
        position = int(action[action.find(",") + 1 : action.find(",)")])
        if target in ["right", "push_box_right", "push_mob_right", "kill_right"]:
            actions += [[position, "d"]]
        elif target in ["left", "push_box_left", "push_mob_left", "kill_left"]:
            actions += [[position, "g"]]
        elif target in ["top", "push_box_top", "push_mob_top", "kill_top"]:
            actions += [[position, "h"]]
        elif target in ["bottom", "push_box_bottom", "push_mob_bottom", "kill_bottom"]:
            actions += [[position, "b"]]
    actions = sorted(actions, key=itemgetter(0))
    for action in actions:
        plan += action[1]

    return plan


def creation_map(infos):
    map = "%% clingo solver_asp.lp\n"

    map += f"#const life = {infos['max_steps']}. \n"
    map += "step(0..life-1).\n"
    wall = []
    demon = []
    for i in range(infos["m"]):
        for j in range(infos["n"]):
            target = infos["grid"][i][j]
            if target == " ":
                map += f"cell({i},{j}).\n"
            elif target == "H":
                map += f"init(at({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "B":
                map += f"init(box({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "#":
                wall.append([i, j])
                # map += f"wall({i},{j}).\n"
            elif target == "D":
                demon.append([i, j])
                # map += f"init(demon({i},{j})).\n"
            elif target == "M":
                map += f"init(mob({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "S":
                map += f"init(spike({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "U":
                map += f"init(trap({i},{j},1)).\n"
                map += f"cell({i},{j}).\n"
            elif target == "T":
                map += f"init(trap({i},{j},0)).\n"
                map += f"cell({i},{j}).\n"
            elif target == "K":
                map += f"init(key({i},{j})).\n"
                map += f"init(keyObtained(0)).\n"
                map += f"cell({i},{j}).\n"
            elif target == "L":
                map += f"init(door({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "O":
                map += f"init(box({i},{j})).\n"
                map += f"init(spike({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "P":
                map += f"init(box({i},{j})).\n"
                map += f"init(trap({i},{j}, 1)).\n"
                map += f"cell({i},{j}).\n"
            elif target == "Q":
                map += f"init(box({i},{j})).\n"
                map += f"init(trap({i},{j}, 0)).\n"
                map += f"cell({i},{j}).\n"

    # ajout des etats finaux
    for coord in demon:
        if [coord[0] + 1, coord[1]] not in wall:
            map += f"goal(at({coord[0]+1},{coord[1]})).\n"
        if [coord[0] - 1, coord[1]] not in wall:
            map += f"goal(at({coord[0]-1},{coord[1]})).\n"
        if [coord[0], coord[1] + 1] not in wall:
            map += f"goal(at({coord[0]},{coord[1]+1})).\n"
        if [coord[0], coord[1] - 1] not in wall:
            map += f"goal(at({coord[0]},{coord[1]-1})).\n"

    with open("asp/helltaker.lp", "r") as f:
        rules = f.read()

    result = map + "\n" + rules
    return result
