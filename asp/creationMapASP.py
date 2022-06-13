def creation_map(infos):
    map = "%% clingo -c horizon=10 -n0 sokorridor.lp"

    map += f"#const n = {infos['max_steps']}."
    wall = []
    demon = []
    for j in range(infos["m"]):
        for i in range(infos["n"]):
            target = infos["grid"][j][i]
            if target == " ":
                map += f"cell({i},{j}).\n"
            elif target == "H":
                map += f"init(at({i},{j})).\n"
            elif target == "B":
                map += f"init(box({i},{j})).\n"
            elif target == "#":
                wall.append([i, j])
            elif target == "D":
                demon.append([i, j])
                map += f"init(demon({i},{j})).\n"
            elif target == "M":
                map += f"init(mob({i},{j})).\n"
            elif target == "S":
                map += f"init(spike({i},{j})).\n"
            elif target == "T":
                map += f"init(trap_safe({i},{j})).\n"
            elif target == "T":
                map += f"init(trap_unsafe({i},{j})).\n"
            elif target == "K":
                map += f"init(key({i},{j})).\n"
            elif target == "L":
                map += f"init(lock({i},{j})).\n"

    # ajout des etats finaux
    for coord in demon:
        if [coord[0] + 1, coord[1]] not in wall:
            map += f"goal(at({coord[0]},{coord[1]})).\n"
        if [coord[0] - 1, coord[1]] not in wall:
            map += f"goal(at({coord[0]},{coord[1]})).\n"
        if [coord[0], coord[1] + 1] not in wall:
            map += f"goal(at({coord[0]},{coord[1]})).\n"
        if [coord[0], coord[1] - 1] not in wall:
            map += f"goal(at({coord[0]},{coord[1]})).\n"

    return map
