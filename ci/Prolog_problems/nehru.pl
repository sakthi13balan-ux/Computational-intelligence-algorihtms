male(motilal_nehru).
male(jawaharlal_nehru).
male(feroze_gandhi).
male(rajiv_gandhi).
male(sanjay_gandhi).
male(rahul_gandhi).
male(varun_gandhi).
male(robert_vadra).
male(raihan_vadra).

female(swarup_rani_nehru).
female(kamala_nehru).
female(indira_gandhi).
female(sonia_gandhi).
female(maneka_gandhi).
female(priyanka_gandhi).
female(miraya_vadra).

married(motilal_nehru, swarup_rani_nehru).
married(jawaharlal_nehru, kamala_nehru).
married(feroze_gandhi, indira_gandhi).
married(rajiv_gandhi, sonia_gandhi).
married(sanjay_gandhi, maneka_gandhi).
married(robert_vadra, priyanka_gandhi).

parent(motilal_nehru, jawaharlal_nehru).
parent(swarup_rani_nehru, jawaharlal_nehru).

parent(jawaharlal_nehru, indira_gandhi).
parent(kamala_nehru, indira_gandhi).

parent(indira_gandhi, rajiv_gandhi).
parent(feroze_gandhi, rajiv_gandhi).

parent(indira_gandhi, sanjay_gandhi).
parent(feroze_gandhi, sanjay_gandhi).

parent(rajiv_gandhi, rahul_gandhi).
parent(sonia_gandhi, rahul_gandhi).

parent(rajiv_gandhi, priyanka_gandhi).
parent(sonia_gandhi, priyanka_gandhi).

parent(sanjay_gandhi, varun_gandhi).
parent(maneka_gandhi, varun_gandhi).

parent(priyanka_gandhi, raihan_vadra).
parent(robert_vadra, raihan_vadra).

parent(priyanka_gandhi, miraya_vadra).
parent(robert_vadra, miraya_vadra).

spouse(X, Y) :- married(X, Y).
spouse(X, Y) :- married(Y, X).

father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).

sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

brother(B, X) :- sibling(B, X), male(B).
sister(S, X) :- sibling(S, X), female(S).

uncle(U, C) :-
    parent(P, C),
    brother(U, P).

aunt(A, C) :-
    parent(P, C),
    sister(A, P).

grandparent(GP, C) :-
    parent(GP, P),
    parent(P, C).

grandfather(GF, C) :- grandparent(GF, C), male(GF).
grandmother(GM, C) :- grandparent(GM, C), female(GM).

nephew(X, Y) :-
    male(X),
    parent(P, X),
    sibling(P, Y).

niece(X, Y) :-
    female(X),
    parent(P, X),
    sibling(P, Y).

cousin(X, Y) :-
    parent(P1, X),
    parent(P2, Y),
    sibling(P1, P2),
    X \= Y.

wife(X, Y) :- spouse(X, Y), female(X).
husband(X, Y) :- spouse(X, Y), male(X).

son(X, Y) :- parent(Y, X), male(X).
daughter(X, Y) :- parent(Y, X), female(X).
child(X, Y) :- parent(Y, X).

relation(X, Y) :-
    father(X, Y), !,
    write(X), write(' is father of '), write(Y).

relation(X, Y) :-
    mother(X, Y), !,
    write(X), write(' is mother of '), write(Y).

relation(X, Y) :-
    brother(X, Y), !,
    write(X), write(' is brother of '), write(Y).

relation(X, Y) :-
    sister(X, Y), !,
    write(X), write(' is sister of '), write(Y).

relation(X, Y) :-
    husband(X, Y), !,
    write(X), write(' is husband of '), write(Y).

relation(X, Y) :-
    wife(X, Y), !,
    write(X), write(' is wife of '), write(Y).

relation(X, Y) :-
    son(X, Y), !,
    write(X), write(' is son of '), write(Y).

relation(X, Y) :-
    daughter(X, Y), !,
    write(X), write(' is daughter of '), write(Y).

relation(X, Y) :-
    uncle(X, Y), !,
    write(X), write(' is uncle of '), write(Y).

relation(X, Y) :-
    aunt(X, Y), !,
    write(X), write(' is aunt of '), write(Y).

relation(X, Y) :-
    grandfather(X, Y), !,
    write(X), write(' is grandfather of '), write(Y).

relation(X, Y) :-
    grandmother(X, Y), !,
    write(X), write(' is grandmother of '), write(Y).

relation(X, Y) :-
    cousin(X, Y), !,
    write(X), write(' is cousin of '), write(Y).

relation(X, Y) :-
    write('No direct relation found').