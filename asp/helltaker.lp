%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%       SOKORRIDOR       %%%
%%%     version: 1.0.0     %%%
%%% author: Sylvain Lagrue %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% clingo -c horizon=10 -n0 helltaker.lp

% pour la gestion de l'horizon
step(0..horizon-1).

% l'environnement : cases vides
cell(0, 0).
cell(1, 0).
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
% cell(3, 2).
cell(3, 3).

% 

%les actions
action(right; left; top; bottom; push_box_right; push_box_left; push_box_top; push_box_bottom; push_mob_right ;push_mob_left; push_mob_top; push_mob_bottom; kill_wall_mob_right; kill_wall_mob_left; kill_wall_mob_top; kill_wall_mob_bottom; kill_box_mob_right; kill_box_mob_left; kill_box_mob_top; kill_box_mob_bottom; waiting).

%%% l'init
init(at(3, 2)).
init(spike(3,1,0)).

fluent(F, 0) :- init(F).

%%% les buts
goal(at(3, 0)).

%%% tous les buts doivent être atteints au pas horizon
:- goal(F), not fluent(F, horizon).

%%% générateur d'actions..
{ do(Act, T): action(Act) } = 1 :- step(T).


%%% les actions
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
    fluent(spike(X, Y, 0), T).


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

fluent(spike(X, Y, 0), T + 1) :-
    do(left, T),
    fluent(spike(X, Y, 1), T).

removed(spike(X, Y, 1), T) :-
    do(left, T),
    fluent(spike(X, Y, 1), T).

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                     waiting                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% waiting      -----------------------------------------------------------------------
% préconditions
:-  do(waiting, T),
    fluent(at(X, Y), T),
    fluent(spike(X, Y, 1), T).

:-  do(waiting, T),
    fluent(at(X, Y), T),
    not fluent(spike(X, Y, 0), T).

% effets
fluent(spike(X, Y, 1), T + 1) :- 
    fluent(spike(X, Y, 0), T),
    do(waiting, T).

removed(spike(X, Y, 0), T) :- 
    fluent(spike(X, Y, 0), T),
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
%                              Tuer le mob sur un mur                                 %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% action kill_wall_mob_left------------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_left, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y - 1), T).

:-  do(kill_wall_mob_left, T), 
    fluent(at(X, Y), T), 
    cell(X, Y - 2).

% effets
removed(mob(X, Y - 1), T) :- 
    do(kill_wall_mob_left, T),
    fluent(at(X, Y), T).

%% action kill_wall_mob_right-----------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y + 1), T).

:-  do(kill_wall_mob_right, T), 
    fluent(at(X, Y), T), 
    cell(X, Y + 2).

% effets
removed(mob(X, Y + 1), T) :- 
    do(kill_wall_mob_right, T),
    fluent(at(X, Y), T).

%% action kill_wall_mob_top------------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X - 1, Y), T).

:-  do(kill_wall_mob_top, T), 
    fluent(at(X, Y), T), 
    cell(X - 2, Y).


% effets
removed(mob(X - 1, Y), T) :- 
    do(kill_wall_mob_top, T),
    fluent(at(X, Y), T).

%% action kill_wall_mob_bottom------------------------------------------------------------------
% préconditions
:-  do(kill_wall_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X + 1, Y), T).

:-  do(kill_wall_mob_bottom, T), 
    fluent(at(X, Y), T), 
    cell(X + 2, Y).

% effets
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

:-  do(kill_box_mob_left, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X, Y - 2), T).

% effets
removed(mob(X, Y - 1), T) :- 
    do(kill_box_mob_left, T),
    fluent(at(X, Y), T).

%% action kill_box_mob_right-----------------------------------------------------------------
% préconditions
:-  do(kill_box_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X, Y + 1), T).

:-  do(kill_box_mob_right, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X, Y + 2), T).

% effets
removed(mob(X, Y + 1), T) :- 
    do(kill_box_mob_right, T),
    fluent(at(X, Y), T).

%% action kill_box_mob_top------------------------------------------------------------------
% préconditions
:-  do(kill_box_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X - 1, Y), T).

:-  do(kill_box_mob_top, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X - 2, Y), T).


% effets
removed(mob(X - 1, Y), T) :- 
    do(kill_box_mob_top, T),
    fluent(at(X, Y), T).

%% action kill_box_mob_bottom------------------------------------------------------------------
% préconditions
:-  do(kill_box_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(mob(X + 1, Y), T).

:-  do(kill_box_mob_bottom, T), 
    fluent(at(X, Y), T), 
    not fluent(box(X + 2, Y), T).

% effets
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
