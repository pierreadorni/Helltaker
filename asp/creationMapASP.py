import subprocess

def exec_asp(filename: str, cmd: str = "clingo", encoding: str = "utf8"):
    result = subprocess.run(
        ["clingo", "test.lp"], capture_output=True
    ).stdout.decode("utf-8")
    chemin =result.split("\n")[4]
    return formater_chemin(chemin)

def formater_chemin(chemin: str):
    chemin = chemin.split(" ")
    actions =[]
    plan =""
    for action in chemin:
        target = action[3:action.find(",")]
        position = action[action.find(","):action.find(",)")]
        if target in ["right", "push_box_right", "push_mob_right", 'kill_right']:
            actions += (position,"r")
        elif target in ["left", "push_box_left", "push_mob_left", 'kill_left']:
            actions += (position,"g")
        elif target in ["top", "push_box_top", "push_mob_top", 'kill_top']:
            actions += (position,"h")
        elif target in ["bottom", "push_box_bottom", "push_mob_bottom", 'kill_bottom']:
            actions += (position,"b")
    actions.sort(key=lambda x: x[0])
    for action in actions:
        plan += action[1]

    return plan



def creation_map(infos):
    map = "%% clingo test.lp\n"

    map += f"#const life = {infos['max_steps']}. \n"
    map +="step(0..life-1).\n"
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
                #map += f"wall({i},{j}).\n"
            elif target == "D":
                demon.append([i, j])
                #map += f"init(demon({i},{j})).\n"
            elif target == "M":
                map += f"init(mob({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "S":
                map += f"init(spike({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "U":
                map += f"init(trap({i},{j}),1).\n"
                map += f"cell({i},{j}).\n"
            elif target == "T":
                map += f"init(trap({i},{j}),0).\n"
                map += f"cell({i},{j}).\n"
            elif target == "K":
                map += f"init(key({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "L":
                map += f"init(door({i},{j})).\n"
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
    map +="""

%%  Les actions-----------------------------------------------------------------------
action(right; left; top; bottom; push_box_right; push_box_left; push_box_top; push_box_bottom; push_mob_right ;push_mob_left; push_mob_top; push_mob_bottom; kill_right; kill_left; kill_top; kill_bottom; waiting).

%%  Les fluents-----------------------------------------------------------------------
fluent(F, 0) :- init(F).

%%  Les condition de victoires--------------------------------------------------------
victory:- goal(F), fluent(F, life).
:- not victory.

%%  Stricement une action par pas ----------------------------------------------------
{ do(Act, T): action(Act) } = 1 :- step(T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Deplacement perso                                      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  action left----------------------------------------------------------------------
% préconditions
:-  do(left, T),
    fluent(at(X, Y), T),
    not cell(X, Y -1).

:-  do(left, T),
    fluent(at(X, Y), T),
    fluent(door(X, Y - 1), T).

:-  do(left, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y - 1), T).

:-  do(left, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y - 1), T).

% effets
fluent(at(X, Y - 1), T + 1) :-
    do(left, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(left, T),
    fluent(at(X, Y), T).

removed(door(A, B), T) :-
    do(left, T),
    fluent(at(X, Y), T),
    fluent(key(X, Y - 1), T),
    fluent(door(A, B), T).

%% action right --------------------------------------------------------------------
% préconditions
:-  do(right, T),
    fluent(at(X, Y), T),
    not cell(X, Y + 1).

:-  do(right, T),
    fluent(at(X, Y), T),
    fluent(door(X, Y + 1), T).

:-  do(right, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y + 1), T).

:-  do(right, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y + 1), T).

% effets
fluent(at(X, Y + 1), T + 1) :-
    do(right, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(right, T),
    fluent(at(X, Y), T).

removed(door(A, B), T) :-
    do(right, T),
    fluent(at(X, Y), T),
    fluent(key(X, Y + 1), T),
    fluent(door(A, B), T).

%% action top  --------------------------------------------------------------------
% préconditions
:-  do(top, T),
    fluent(at(X, Y), T),
    not cell(X - 1, Y).

:-  do(top, T),
    fluent(at(X, Y), T),
    fluent(door(X - 1, Y), T).

:-  do(top, T),
    fluent(at(X, Y), T),
    fluent(box(X - 1, Y), T).

:-  do(top, T),
    fluent(at(X, Y), T),
    fluent(mob(X - 1, Y), T).

% effets
fluent(at(X - 1, Y), T + 1) :-
    do(top, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(top, T),
    fluent(at(X, Y), T).

removed(door(A, B), T) :-
    do(top, T),
    fluent(at(X, Y), T),
    fluent(key(X - 1, Y), T),
    fluent(door(A, B), T).

%% action bottom  --------------------------------------------------------------------
% préconditions
:-  do(bottom, T),
    fluent(at(X, Y), T),
    not cell(X + 1, Y).

:-  do(bottom, T),
    fluent(at(X, Y), T),
    fluent(door(X + 1, Y), T).

:-  do(bottom, T),
    fluent(at(X, Y), T),
    fluent(box(X + 1, Y), T).

:-  do(bottom, T),
    fluent(at(X, Y), T),
    fluent(mob(X + 1, Y), T).

% effets
fluent(at(X + 1, Y), T + 1) :-
    do(bottom, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(bottom, T),
    fluent(at(X, Y), T).

removed(door(A, B), T) :-
    do(bottom, T),
    fluent(at(X, Y), T),
    fluent(key(X + 1, Y), T),
    fluent(door(A, B), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                     waiting                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% waiting      -----------------------------------------------------------------------
% préconditions
:-  do(waiting, T),
    fluent(at(X, Y), T),
    not fluent(spike(X, Y), T); not fluent(trap(X, Y, 1), T).

% effets
fluent(spike(X, Y), T + 2) :-
    fluent(spike(X, Y), T),
    fluent(at(X, Y), T),
    do(waiting, T).

removed(spike(X, Y), T) :-
    fluent(spike(X, Y), T),
    fluent(at(X, Y), T),
    do(waiting, T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Pousser la boite                                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action push_box_left----------------------------------------------------------------
% préconditions
:-  do(push_box_left, T),
    fluent(at(X, Y), T),
    not fluent(box(X, Y - 1), T).

:-  do(push_box_left, T),
    fluent(at(X, Y), T),
    not cell(X, Y - 2).

:-  do(push_box_left, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y - 2), T).

:-  do(push_box_left, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y - 2), T).

% effets
fluent(box(X, Y - 2), T + 1) :-
    do(push_box_left, T),
    fluent(at(X, Y), T).

removed(box(X, Y - 1), T) :-
    do(push_box_left, T),
    fluent(at(X, Y), T).

%% action push_box_right-----------------------------------------------------------------
% préconditions
:-  do(push_box_right, T),
    fluent(at(X, Y), T),
    not fluent(box(X, Y + 1), T).

:-  do(push_box_right, T),
    fluent(at(X, Y), T),
    not cell(X, Y + 2).

:-  do(push_box_right, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y + 2), T).

:-  do(push_box_right, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y + 2), T).

% effets
fluent(box(X, Y + 2), T + 1) :-
    do(push_box_right, T),
    fluent(at(X, Y), T).

removed(box(X, Y + 1), T) :-
    do(push_box_right, T),
    fluent(at(X, Y), T).

%% action push_box_top------------------------------------------------------------------
% préconditions
:-  do(push_box_top, T),
    fluent(at(X, Y), T),
    not fluent(box(X - 1, Y), T).

:-  do(push_box_top, T),
    fluent(at(X, Y), T),
    not cell(X - 2, Y).

:-  do(push_box_top, T),
    fluent(at(X, Y), T),
    fluent(box(X - 2, Y), T).

:-  do(push_box_top, T),
    fluent(at(X, Y), T),
    fluent(mob(X - 2, Y), T).

% effets
fluent(box(X - 2, Y), T + 1) :-
    do(push_box_top, T),
    fluent(at(X, Y), T).

removed(box(X - 1, Y), T) :-
    do(push_box_top, T),
    fluent(at(X, Y), T).

%% action push_box_bottom------------------------------------------------------------------
% préconditions
:-  do(push_box_bottom, T),
    fluent(at(X, Y), T),
    not fluent(box(X + 1, Y), T).

:-  do(push_box_bottom, T),
    fluent(at(X, Y), T),
    not cell(X + 2, Y).

:-  do(push_box_bottom, T),
    fluent(at(X, Y), T),
    fluent(box(X + 2, Y), T).

:-  do(push_box_bottom, T),
    fluent(at(X, Y), T),
    fluent(mob(X + 2, Y), T).

% effets
fluent(box(X + 2, Y), T + 1) :-
    do(push_box_bottom, T),
    fluent(at(X, Y), T).

removed(box(X + 1, Y), T) :-
    do(push_box_bottom, T),
    fluent(at(X, Y), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Pousser un mob                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action push_mob_left------------------------------------------------------------------
% préconditions
:-  do(push_mob_left, T),
    fluent(at(X, Y), T),
    not fluent(mob(X, Y - 1), T).

:-  do(push_mob_left, T),
    fluent(at(X, Y), T),
    not cell(X, Y - 2).

:-  do(push_mob_left, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y - 2), T).

:-  do(push_mob_left, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y - 2), T).

% effets
fluent(mob(X, Y - 2), T + 1) :-
    do(push_mob_left, T),
    fluent(at(X, Y), T).

removed(mob(X, Y - 1), T) :-
    do(push_mob_left, T),
    fluent(at(X, Y), T).

%% action push_mob_right-----------------------------------------------------------------
% préconditions
:-  do(push_mob_right, T),
    fluent(at(X, Y), T),
    not fluent(mob(X, Y + 1), T).

:-  do(push_mob_right, T),
    fluent(at(X, Y), T),
    not cell(X, Y + 2).

:-  do(push_mob_right, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y + 2), T).

:-  do(push_mob_right, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y + 2), T).

% effets
fluent(mob(X, Y + 2), T + 1) :-
    do(push_mob_right, T),
    fluent(at(X, Y), T).

removed(mob(X, Y + 1), T) :-
    do(push_mob_right, T),
    fluent(at(X, Y), T).

%% action push_mob_top------------------------------------------------------------------
% préconditions
:-  do(push_mob_top, T),
    fluent(at(X, Y), T),
    not fluent(mob(X - 1, Y), T).

:-  do(push_mob_top, T),
    fluent(at(X, Y), T),
    not cell(X - 2, Y).

:-  do(push_mob_top, T),
    fluent(at(X, Y), T),
    fluent(mob(X - 2, Y), T).

:-  do(push_mob_top, T),
    fluent(at(X, Y), T),
    fluent(box(X - 2, Y), T).

% effets
fluent(mob(X - 2, Y), T + 1) :-
    do(push_mob_top, T),
    fluent(at(X, Y), T).

removed(mob(X - 1, Y), T) :-
    do(push_mob_top, T),
    fluent(at(X, Y), T).

%% action push_mob_bottom------------------------------------------------------------------
% préconditions
:-  do(push_mob_bottom, T),
    fluent(at(X, Y), T),
    not fluent(mob(X + 1, Y), T).

:-  do(push_mob_bottom, T),
    fluent(at(X, Y), T),
    not cell(X + 2, Y).

:-  do(push_mob_bottom, T),
    fluent(at(X, Y), T),
    fluent(mob(X + 2, Y), T).

:-  do(push_mob_bottom, T),
    fluent(at(X, Y), T),
    fluent(box(X + 2, Y), T).

% effets
fluent(mob(X + 2, Y), T + 1) :-
    do(push_mob_bottom, T),
    fluent(at(X, Y), T).

removed(mob(X + 1, Y), T) :-
    do(push_mob_bottom, T),
    fluent(at(X, Y), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                     Tuer un mob                                     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action kill_left------------------------------------------------------------------
% préconditions
:-  do(kill_left, T),
    fluent(at(X, Y), T),
    not fluent(mob(X, Y - 1), T).

:-  do(kill_left, T),
    fluent(at(X, Y), T),
    cell(X, Y - 2); not fluent(box(X, Y - 2), T).

% effets
removed(mob(X, Y - 1), T) :-
    do(kill_left, T),
    fluent(at(X, Y), T).

%% action kill_right-----------------------------------------------------------------
% préconditions
:-  do(kill_right, T),
    fluent(at(X, Y), T),
    not fluent(mob(X, Y + 1), T).

:-  do(kill_right, T),
    fluent(at(X, Y), T),
    cell(X, Y + 2); not fluent(box(X, Y + 2), T).

% effets

removed(mob(X, Y + 1), T) :-
    do(kill_right, T),
    fluent(at(X, Y), T).

%% action kill_top------------------------------------------------------------------
% préconditions
:-  do(kill_top, T),
    fluent(at(X, Y), T),
    not fluent(mob(X - 1, Y), T).

:-  do(kill_top, T),
    fluent(at(X, Y), T),
    cell(X - 2, Y); not fluent(box(X - 2, Y), T).


% effets

removed(mob(X - 1, Y), T) :-
    do(kill_top, T),
    fluent(at(X, Y), T).

%% action kill_bottom------------------------------------------------------------------
% préconditions
:-  do(kill_bottom, T),
    fluent(at(X, Y), T),
    not fluent(mob(X + 1, Y), T).

:-  do(kill_bottom, T),
    fluent(at(X, Y), T),
    cell(X + 2, Y); not fluent(box(X + 2, Y), T).

% effets

removed(mob(X + 1, Y), T) :-
    do(kill_bottom, T),
    fluent(at(X, Y), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Gestion des Trap                                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


fluent(trap(X, Y, 1), T + 1) :-
    do(Act, T),
    Act != waiting,
    fluent(trap(X, Y, 0), T).

fluent(trap(X, Y, 0), T + 1) :-
    do(Act, T),
    Act != waiting,
    fluent(trap(X, Y, 1), T).

fluent(trap(X, Y, 0), T + 2) :-
    do(waiting, T),
    fluent(at(X, Y), T),
    fluent(trap(X, Y, 1), T).


fluent(trap(X, Y, 1), T + 2) :-
    do(waiting, T),
    fluent(at(X, Y), T),
    fluent(trap(X, Y, 0), T).

fluent(trap(X, Y, E), T + 1) :-
    do(waiting, T),
    not fluent(at(X, Y), T),
    fluent(trap(X, Y, E), T).

removed(trap(X, Y, E), T) :-
    do(Act, T),
    fluent(trap(X, Y, E), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                   Macro commandes                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Attendre si sur un pic--------------------------------------------------------------
:- do(Act, T),
    Act != waiting,
    fluent(at(X, Y), T),
    fluent(trap(X, Y, 1), T).

:- do(Act, T),
    Act != waiting,
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

%% Creation Fluent en T + 1--------------------------------------------------------------
% Non spike
fluent(F, T + 1) :-
    fluent(F, T),
    F != spike,
    T + 1 <= life,
    not removed(F, T).


% Spike
fluent(F, T + 1) :-
    fluent(F, T),
    F = spike(X, Y),
    fluent(at(X, Y), T),
    not do(waiting, T),
    T + 1 <= life.

#show do/2.
"""
    return map