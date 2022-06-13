%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%       SOKORRIDOR       %%%
%%%     version: 1.0.0     %%%
%%% author: Sylvain Lagrue %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% clingo -c horizon=10 -n0 sokorridor.lp

% la taille du monde
#const n = 6. 

% pour la gestion de l'horizon
step(0..horizon-1).

% l'environnement : cases vides
cell(0, 0).
% cell(1, 0).
cell(2, 0).
cell(3, 0).
cell(0, 1).
cell(0, 2).
cell(0, 3).
cell(1, 1).
cell(2, 1).
cell(3, 1).
cell(1, 2).
cell(1, 3).
cell(2, 2).
cell(2, 3).
cell(3, 2).
cell(3, 3).

% 

%les actions
action(right; left; top; bottom; push_box_right; push_box_left; push_box_top; push_box_bottom; push_mob_right ;push_mob_left; push_mob_top; push_mob_bottom; kill_mob_right; kill_mob_left; kill_mob_top; kill_mob_bottom).

%%% l'init
init(at(3, 0)).
init(box(2, 0)).
ini(box(3, 1)).

fluent(F, 0) :- init(F).

%%% les buts
goal(at(1, 2)).

%%% tous les buts doivent être atteints au pas horizon
:- goal(F), not fluent(F, horizon).

%%% générateur d'actions..
{ do(Act, T): action(Act) } = 1 :- step(T).

%%% les actions
%%  action left----------------------------------------------------------------------
% préconditions
:-  do(left, T), 
    fluent(at(X, Y), T), 
    not cell(X, Y -1). 

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

%% action right --------------------------------------------------------------------
% préconditions
:-  do(right, T), 
    fluent(at(X, Y), T),
    not cell(X, Y + 1).

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

%% action top  --------------------------------------------------------------------
% préconditions
:-  do(top, T), 
    fluent(at(X, Y), T),
    not cell(X - 1, Y).

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

%% action bottom  --------------------------------------------------------------------
% préconditions
:-  do(bottom, T), 
    fluent(at(X, Y), T),
    not cell(X + 1, Y).

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

%% action push_box_left------------------------------------------------------------------
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

%% action kill_mob_left------------------------------------------------------------------
% préconditions
:-  do(kill_mob_left, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y - 1), T).

:-  do(kill_mob_left, T), 
    fluent(at(X, Y), T), 
    cell(X, Y - 2).

% effets
removed(mob(X, Y - 1), T) :- 
    do(kill_mob_left, T),
    fluent(at(X, Y), T).

%% action kill_mob_right-----------------------------------------------------------------
% préconditions
:-  do(kill_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y + 1), T).

:-  do(kill_mob_right, T), 
    fluent(at(X, Y), T), 
    cell(X, Y + 2).

% effets
removed(mob(X, Y + 1), T) :- 
    do(kill_mob_right, T),
    fluent(at(X, Y), T).

%% action kill_mob_top------------------------------------------------------------------
% préconditions
:-  do(kill_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X - 1, Y), T).

:-  do(kill_mob_top, T), 
    fluent(at(X, Y), T), 
    cell(X - 2, Y).


% effets
removed(mob(X - 1, Y), T) :- 
    do(kill_mob_top, T),
    fluent(at(X, Y), T).

%% action kill_mob_bottom------------------------------------------------------------------
% préconditions
:-  do(kill_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X + 1, Y), T).

:-  do(kill_mob_bottom, T), 
    fluent(at(X, Y), T), 
    cell(X + 2, Y).

% effets
removed(mob(X + 1, Y), T) :- 
    do(kill_mob_bottom, T),
    fluent(at(X, Y), T).


%%% Frame Problem
% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(F, T + 1) :- 
    fluent(F, T), 
    T + 1 <= horizon,
    not removed(F, T).

#show do/2.
