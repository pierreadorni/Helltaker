%% clingo solver_asp.lp
#const life = 12. 
step(0..life-1).
cell(1,1).
cell(1,2).
cell(1,8).
cell(1,9).
cell(2,1).
cell(2,2).
cell(2,3).
cell(2,4).
init(mob(2,5)).
cell(2,5).
cell(2,6).
cell(2,7).
cell(2,8).
cell(2,9).
cell(3,1).
cell(3,2).
cell(3,3).
cell(3,4).
init(mob(3,5)).
cell(3,5).
cell(3,6).
cell(3,7).
cell(3,8).
cell(3,9).
cell(4,1).
cell(4,2).
cell(4,4).
init(mob(4,5)).
cell(4,5).
cell(4,6).
cell(4,8).
cell(4,9).
cell(5,1).
cell(5,2).
cell(5,3).
cell(5,4).
init(mob(5,5)).
cell(5,5).
cell(5,6).
cell(5,7).
cell(5,8).
cell(5,9).
cell(6,1).
cell(6,2).
cell(6,4).
init(mob(6,5)).
cell(6,5).
cell(6,6).
cell(6,8).
cell(6,9).
cell(7,1).
cell(7,2).
cell(7,3).
cell(7,4).
init(mob(7,5)).
cell(7,5).
cell(7,6).
cell(7,7).
cell(7,8).
cell(7,9).
cell(8,2).
cell(8,4).
init(mob(8,5)).
cell(8,5).
cell(8,6).
cell(8,8).
cell(9,2).
cell(9,3).
cell(9,4).
init(mob(9,5)).
cell(9,5).
cell(9,6).
cell(9,7).
cell(9,8).
cell(10,2).
cell(10,4).
cell(10,5).
cell(10,6).
cell(10,8).
cell(11,2).
cell(11,3).
cell(11,4).
init(at(11,5)).
cell(11,5).
cell(11,6).
cell(11,7).
cell(11,8).
cell(12,4).
cell(12,5).
cell(12,6).
goal(at(2,5)).

%%  Les actions-----------------------------------------------------------------------
action(right; left; top; bottom; push_box_right; push_box_left; push_box_top; push_box_bottom; push_mob_right ;push_mob_left; push_mob_top; push_mob_bottom; kill_right; kill_left; kill_top; kill_bottom; waiting).
push_bot(push_mob_right; push_mob_left; push_mob_top; push_mob_bottom).
%%  Les fluents-----------------------------------------------------------------------
fluent(F, 0) :- init(F).

%%  Les condition de victoires--------------------------------------------------------
victory:- goal(F), fluent(F, life).
:- not victory.

%%  La recuperation de la clef---------------------------------------------------------
fluent(keyObtained(1), T + 1):-
    fluent(at(X, Y),T),
    fluent(key(X, Y), T),
    fluent(keyObtained(0), T).

removed(keyObtained(0), T):-
    fluent(at(X, Y),T),
    fluent(key(X, Y), T),
    fluent(keyObtained(0), T).

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
    fluent(door(X, Y - 1), T),
    not fluent(keyObtained(1), T).

:-  do(left, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y - 1), T).

:-  do(left, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y - 1), T),
    not fluent(trap(X, Y - 1, 1), T).

% effets
fluent(at(X, Y - 1), T + 1) :-
    do(left, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(left, T),
    fluent(at(X, Y), T).

removed(door(X, Y - 1) , T):-
    do(left, T),
    fluent(at(X, Y), T),
    fluent(door(X, Y - 1), T),
    fluent(keyObtained(1), T).

%% action right --------------------------------------------------------------------
% préconditions
:-  do(right, T),
    fluent(at(X, Y), T),
    not cell(X, Y + 1).

:-  do(right, T),
    fluent(at(X, Y), T),
    fluent(door(X, Y + 1), T),
    not fluent(keyObtained(1), T).

:-  do(right, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y + 1), T).

:-  do(right, T),
    fluent(at(X, Y), T),
    fluent(mob(X, Y + 1), T),
    not fluent(trap(X, Y + 1, 1), T).

% effets
fluent(at(X, Y + 1), T + 1) :-
    do(right, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(right, T),
    fluent(at(X, Y), T).

removed(door(X, Y + 1) , T):-
    do(right, T),
    fluent(at(X, Y), T),
    fluent(door(X, Y + 1), T),
    fluent(keyObtained(1), T).

%% action top  --------------------------------------------------------------------
% préconditions
:-  do(top, T),
    fluent(at(X, Y), T),
    not cell(X - 1, Y).

:-  do(top, T),
    fluent(at(X, Y), T),
    fluent(door(X - 1, Y), T),
    not fluent(keyObtained(1), T).

:-  do(top, T),
    fluent(at(X, Y), T),
    fluent(box(X - 1, Y), T).

:-  do(top, T),
    fluent(at(X, Y), T),
    fluent(mob(X - 1, Y), T),
    not fluent(trap(X - 1, Y, 1), T).

% effets
fluent(at(X - 1, Y), T + 1) :-
    do(top, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(top, T),
    fluent(at(X, Y), T).

removed(door(X - 1, Y) , T):-
    do(top, T),
    fluent(at(X, Y), T),
    fluent(door(X - 1, Y), T),
    fluent(keyObtained(1), T).

%% action bottom  --------------------------------------------------------------------
% préconditions
:-  do(bottom, T),
    fluent(at(X, Y), T),
    not cell(X + 1, Y).

:-  do(bottom, T),
    fluent(at(X, Y), T),
    fluent(door(X + 1, Y), T),
    not fluent(keyObtained(1), T).

:-  do(bottom, T),
    fluent(at(X, Y), T),
    fluent(box(X + 1, Y), T).

:-  do(bottom, T),
    fluent(at(X, Y), T),
    fluent(mob(X + 1, Y), T),
    not fluent(trap(X + 1, Y, 1), T).

% effets
fluent(at(X + 1, Y), T + 1) :-
    do(bottom, T),
    fluent(at(X, Y), T).

removed(at(X, Y), T) :-
    do(bottom, T),
    fluent(at(X, Y), T).

removed(door(X + 1, Y) , T):-
    do(bottom, T),
    fluent(at(X, Y), T),
    fluent(door(X + 1, Y), T),
    fluent(keyObtained(1), T).

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
    fluent(door(X, Y - 2), T).

:-  do(push_box_left, T),
    fluent(at(X, Y), T),
    not cell(X, Y - 2).

:-  do(push_box_left, T),
    fluent(at(X, Y), T),
    fluent(box(X, Y - 2), T).

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
    fluent(door(X, Y + 2), T).

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
    fluent(door(X - 2, Y), T).

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
    fluent(door(X + 2, Y), T).

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
    fluent(door(X, Y - 2), T).

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
    fluent(door(X, Y + 2), T).

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
    fluent(door(X - 2, Y), T).

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
    fluent(door(X + 2, Y), T).

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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                     Tuer un mob                                     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% kill mob if on trap---------------------------------------------------------------

removed(mob(X, Y), T) :-
    fluent(trap(X, Y, 1), T),
    fluent(mob(X, Y), T).

removed(mob(X, Y), T) :-
    fluent(spike(X, Y), T),
    fluent(mob(X, Y), T).

%% action kill_left------------------------------------------------------------------
% préconditions
:-  do(kill_left, T),
    fluent(at(X, Y), T),
    not fluent(mob(X, Y - 1), T).

:-  do(kill_left, T),
    fluent(at(X, Y), T),
    cell(X, Y - 2); not fluent(box(X, Y - 2), T); not fluent(door(X, Y - 2), T).

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
    cell(X, Y + 2); not fluent(box(X, Y + 2), T); not fluent(door(X, Y + 2), T).

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
    cell(X - 2, Y); not fluent(box(X - 2, Y), T); not fluent(door(X - 2, Y), T).

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
    cell(X + 2, Y); not fluent(box(X + 2, Y), T); not fluent(door(X + 2, Y), T).

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