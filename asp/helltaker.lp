%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                  HELLTAKER                                             %
%                                     IA02                                               %
%                             author: PA, AL, RD                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%clingo -c life=5 helltaker.lp

%%  Declaration des règles du jeu-----------------------------------------------------
%%  Le temps--------------------------------------------------------------------------
#const life = 23.
step(0..life-1).

%%  Les cases vides-------------------------------------------------------------------
cell(1,4).
cell(2,3).
cell(2,4).
init(box(2,5)).
cell(2,5).
cell(2,6).
init(at(3,1)).
cell(3,1).
init(trap(3,3,1)).
cell(3,3).
cell(3,4).
init(box(3,5)).
cell(3,5).
cell(3,6).
cell(4,1).
cell(4,3).
init(trap(4,4,1)).
cell(4,4).
cell(4,5).
init(trap(4,6,1)).
cell(4,6).
init(mob(5, 1)).
cell(5,1).
init(box(5,3)).
cell(5,3).
init(box(5,4)).
cell(5,4).
init(box(5,5)).
cell(5,5).
init(box(5,6)).
cell(5,6).
init(trap(6,1,0)).
cell(6,1).
cell(6,2).
init(trap(6,3,0)).
cell(6,3).
cell(6,4).
cell(6,5).
init(trap(6,6,0)).
cell(6,6).
cell(7,6).
goal(at(2,5)).
goal(at(1,4)).
%%  Les cases occupées----------------------------------------------------------------
%trap(X, Y, E) : si E = 1, le trap est actif en T=0


%%  Le but----------------------------------------------------------------------------
goal(at(3, 3)).

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
    not fluent(trap(X + 2, Y, 0), T),
    do(push_mob_bottom, T),
    fluent(at(X, Y), T).

fluent(mob(X + 2, Y), T + 1) :-
    not fluent(trap(X + 2, Y, 1), T),
    do(push_mob_bottom, T),
    fluent(at(X, Y), T).

removed(mob(X + 1, Y), T) :-
    do(push_mob_bottom, T),
    fluent(at(X, Y), T).

removed(mob(X + 1, Y), T) :-
    do(push_mob_bottom, T),
    fluent(trap(X + 1, Y, E), T),
    fluent(at(X, Y), T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                     Tuer un mob                                     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% kill mob if on trap---------------------------------------------------------------
removed(mob(X, Y), T) :-
    fluent(trap(X, Y, 0), T),
    fluent(mob(X, Y), T).

removed(mob(X, Y), T) :-
    fluent(trap(X, Y, 1), T),
    fluent(mob(X, Y), T).

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
    fluent(trap(X + 1, Y, E), T).

:-  do(kill_bottom, T),
    fluent(at(X, Y), T),
    cell(X + 2, Y); not fluent(box(X + 2, Y), T).

:-  do(kill_bottom, T),
    fluent(at(X, Y), T),
    fluent(mob(X + 1, Y), T),
    not fluent(trap(X + 1, Y, 1), T).

:-  do(kill_bottom, T),
    fluent(at(X, Y), T),
    fluent(mob(X + 1, Y), T),
    not fluent(trap(X + 1, Y, 0), T).


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
    fluent(trap(X, Y, 1), T).

fluent(trap(X, Y, 1), T + 2) :-
    do(waiting, T),
    fluent(trap(X, Y, 0), T).

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
