import subprocess

def exec_asp(filename: str, cmd: str = "clingo", encoding: str = "utf8"):
    result = subprocess.run(
        ["clingo", "test.lp"], capture_output=True
    ).stdout.decode("utf-8")
    chemin =result.split("\n")[4]
    return formater_chemin(chemin)

def formater_chemin(chemin: str):
    chemin = chemin.split(" ")
    plan =""
    for action in chemin:
        target = action[3:action.find(",")]
        if target in ["right", "push_box_right", "push_mob_right", "kill_wall_mob_right"]:
            plan += "d"
        elif target in ["left", "push_box_left", "push_mob_left", "kill_wall_mob_left"]:
            plan += "g"
        elif target in ["top", "push_box_top", "push_mob_top", "kill_wall_mob_top"]:
            plan += "h"
        elif target in ["bottom", "push_box_bottom", "push_mob_bottom", "kill_wall_mob_bottom"]:
            plan += "b"
    return plan



def creation_map(infos):
    map = "%% clingo test.lp\n"

    map += f"#const horizon = {infos['max_steps']}. \n"
    map +="step(0..horizon-1).\n"
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
            elif target == "D":
                demon.append([i, j])
                #map += f"init(demon({i},{j})).\n"
            elif target == "M":
                map += f"init(mob({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "S":
                map += f"init(spike({i},{j})).\n"
                map += f"cell({i},{j}).\n"
            elif target == "T":
                map += f"init(trap_safe({i},{j}),1).\n"
                map += f"cell({i},{j}).\n"
            elif target == "T":
                map += f"init(trap_unsafe({i},{j}),0).\n"
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
%les actions
action(right; left; top; bottom; push_box_right; push_box_left; push_box_top; push_box_bottom; push_mob_right ;push_mob_left; push_mob_top; push_mob_bottom; kill_wall_mob_right; kill_wall_mob_left; kill_wall_mob_top; kill_wall_mob_bottom; kill_box_mob_right; kill_box_mob_left; kill_box_mob_top; kill_box_mob_bottom; waiting).

%%% l'init, format (X, Y); (X, Y, E) avec E etat (0 : coupant->spike, fermé->door, à terre -> clé)


fluent(F, 0) :- init(F).

%%% les buts

%%% On gagne s'il l'un des buts est atteint
victory:- goal(F), fluent(F, horizon).
:- not victory.

%%% générateur d'actions..
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
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(left, T),
    fluent(spike(X, Y), T).

removed(spike(X, Y), T) :-
    do(left, T),
    fluent(spike(X, Y), T).

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

:- do(right, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(right, T),
    fluent(spike(X, Y), T).

removed(at(X, Y), T) :- 
    do(right, T), 
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(right, T),
    fluent(spike(X, Y), T).

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
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(top, T),
    fluent(spike(X, Y), T).

removed(at(X, Y), T) :- 
    do(top, T), 
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(top, T),
    fluent(spike(X, Y), T).

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
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(bottom, T),
    fluent(spike(X, Y), T).

removed(at(X, Y), T) :- 
    do(bottom, T), 
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(bottom, T),
    fluent(spike(X, Y), T).

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
    not fluent(spike(X, Y), T).

% effets
fluent(spike(X, Y), T + 2) :- 
    fluent(spike(X, Y), T),
    do(waiting, T).

removed(spike(X, Y), T) :- 
    fluent(spike(X, Y), T),
    do(waiting, T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Pousser la boite                                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action push_box_left----------------------------------------------------------------
% préconditions
:-  do(push_box_left, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X, Y - 1), T).

:- do(push_box_left, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_box_left, T),
    fluent(spike(X, Y), T).

removed(box(X, Y - 1), T) :- 
    do(push_box_left, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_box_left, T),
    fluent(spike(X, Y), T).

%% action push_box_right-----------------------------------------------------------------
% préconditions
:-  do(push_box_right, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X, Y + 1), T).

:-  do(push_box_right, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_box_right, T),
    fluent(spike(X, Y), T).

removed(box(X, Y + 1), T) :- 
    do(push_box_right, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_box_right, T),
    fluent(spike(X, Y), T).

%% action push_box_top------------------------------------------------------------------
% préconditions
:-  do(push_box_top, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X - 1, Y), T).

:-  do(push_box_top, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_box_top, T),
    fluent(spike(X, Y), T).

removed(box(X - 1, Y), T) :- 
    do(push_box_top, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_box_top, T),
    fluent(spike(X, Y), T).

%% action push_box_bottom------------------------------------------------------------------
% préconditions
:-  do(push_box_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X + 1, Y), T).

:-  do(push_box_bottom, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_box_bottom, T),
    fluent(spike(X, Y), T).

removed(box(X + 1, Y), T) :- 
    do(push_box_bottom, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_box_bottom, T),
    fluent(spike(X, Y), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Pousser un mob                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action push_mob_left------------------------------------------------------------------
% préconditions
:-  do(push_mob_left, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y - 1), T).

:- do(push_mob_left, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_mob_left, T),
    fluent(spike(X, Y), T).

removed(mob(X, Y - 1), T) :- 
    do(push_mob_left, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_mob_left, T),
    fluent(spike(X, Y), T).

%% action push_mob_right-----------------------------------------------------------------
% préconditions
:-  do(push_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y + 1), T).

:- do(push_mob_right, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_mob_right, T),
    fluent(spike(X, Y), T).

removed(mob(X, Y + 1), T) :- 
    do(push_mob_right, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_mob_right, T),
    fluent(spike(X, Y), T).

%% action push_mob_top------------------------------------------------------------------
% préconditions
:-  do(push_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X - 1, Y), T).

:- do(push_mob_top, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_mob_top, T),
    fluent(spike(X, Y), T).

removed(mob(X - 1, Y), T) :- 
    do(push_mob_top, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_mob_top, T),
    fluent(spike(X, Y), T).

%% action push_mob_bottom------------------------------------------------------------------
% préconditions
:-  do(push_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X + 1, Y), T).

:- do(push_mob_bottom, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

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

fluent(spike(X, Y), T + 1) :-
    do(push_mob_bottom, T),
    fluent(spike(X, Y), T).

removed(mob(X + 1, Y), T) :- 
    do(push_mob_bottom, T),
    fluent(at(X, Y), T).

removed(spike(X, Y), T) :-
    do(push_mob_bottom, T),
    fluent(spike(X, Y), T).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Tuer le mob sur un mur                                 %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action kill_wall_mob_left------------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_left, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y - 1), T).

:- do(kill_wall_mob_left, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

:-  do(kill_wall_mob_left, T), 
    fluent(at(X, Y), T), 
    cell(X, Y - 2).

% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_wall_mob_left, T),
    fluent(spike(X, Y), T).

removed(spike(X, Y), T) :-
    do(kill_wall_mob_left, T),
    fluent(spike(X, Y), T).

removed(mob(X, Y - 1), T) :-
    do(kill_wall_mob_left, T),
    fluent(at(X, Y), T).

%% action kill_wall_mob_right-----------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y + 1), T).

:- do(kill_wall_mob_right, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

:-  do(kill_wall_mob_right, T), 
    fluent(at(X, Y), T), 
    cell(X, Y + 2).

% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_wall_mob_right, T),
    fluent(spike(X, Y), T).

removed(spike(X, Y), T) :-
    do(kill_wall_mob_right, T),
    fluent(spike(X, Y), T).

removed(mob(X, Y + 1), T) :- 
    do(kill_wall_mob_right, T),
    fluent(at(X, Y), T).

%% action kill_wall_mob_top------------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X - 1, Y), T).

:- do(kill_wall_mob_top, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

:-  do(kill_wall_mob_top, T), 
    fluent(at(X, Y), T), 
    cell(X - 2, Y).


% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_wall_mob_top, T),
    fluent(spike(X, Y), T).

removed(spike(X, Y), T) :-
    do(kill_wall_mob_top, T),
    fluent(spike(X, Y), T).

removed(mob(X - 1, Y), T) :- 
    do(kill_wall_mob_top, T),
    fluent(at(X, Y), T).

%% action kill_wall_mob_bottom------------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X + 1, Y), T).

:- do(kill_wall_mob_bottom, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

:-  do(kill_wall_mob_bottom, T), 
    fluent(at(X, Y), T), 
    cell(X + 2, Y).

% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_wall_mob_bottom, T),
    fluent(spike(X, Y), T).

removed(spike(X, Y), T) :-
    do(kill_wall_mob_bottom, T),
    fluent(spike(X, Y), T).

removed(mob(X + 1, Y), T) :- 
    do(kill_wall_mob_bottom, T),
    fluent(at(X, Y), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              Tuer le mob sur un block                               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action kill_box_mob_left------------------------------------------------------------------
% préconditions
:-  do(kill_box_mob_left, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y - 1), T).

:- do(kill_box_mob_left, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).

:-  do(kill_box_mob_left, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X, Y - 2), T).

% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_box_mob_left, T),
    fluent(spike(X, Y), T).
removed(spike(X, Y), T) :-
    do(kill_box_mob_left, T),
    fluent(spike(X, Y), T).
removed(mob(X, Y - 1), T) :- 
    do(kill_box_mob_left, T),
    fluent(at(X, Y), T).

%% action kill_box_mob_right-----------------------------------------------------------------
% préconditions
:-  do(kill_box_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y + 1), T).
:- do(kill_box_mob_right, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).
:-  do(kill_box_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X, Y + 2), T).

% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_box_mob_right, T),
    fluent(spike(X, Y), T).
removed(spike(X, Y), T) :-
    do(kill_box_mob_right, T),
    fluent(spike(X, Y), T).
removed(mob(X, Y + 1), T) :- 
    do(kill_box_mob_right, T),
    fluent(at(X, Y), T).

%% action kill_box_mob_top------------------------------------------------------------------
% préconditions
:-  do(kill_box_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X - 1, Y), T).
:- do(kill_box_mob_top, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).
:-  do(kill_box_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X - 2, Y), T).


% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_box_mob_top, T),
    fluent(spike(X, Y), T).
removed(spike(X, Y), T) :-
    do(kill_box_mob_top, T),
    fluent(spike(X, Y), T).
removed(mob(X - 1, Y), T) :- 
    do(kill_box_mob_top, T),
    fluent(at(X, Y), T).

%% action kill_box_mob_bottom------------------------------------------------------------------
% préconditions
:-  do(kill_box_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X + 1, Y), T).
:- do(kill_box_mob_bottom, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y), T).
:-  do(kill_box_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X + 2, Y), T).

% effets
fluent(spike(X, Y), T + 1) :-
    do(kill_box_mob_bottom, T),
    fluent(spike(X, Y), T).
removed(spike(X, Y), T) :-
    do(kill_box_mob_bottom, T),
    fluent(spike(X, Y), T).
removed(mob(X + 1, Y), T) :- 
    do(kill_box_mob_bottom, T),
    fluent(at(X, Y), T).

%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F, T + 1) :- 
    fluent(F, T), 
    T + 1 <= horizon,
    not removed(F, T).

#show do/2.
"""
    return map
