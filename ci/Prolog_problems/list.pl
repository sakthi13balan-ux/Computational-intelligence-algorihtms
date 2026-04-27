% ---------- BASIC OPERATIONS ----------

mymember(X, [X|_]).
mymember(X, [_|T]) :- mymember(X, T).

subset([], _).
subset([H|T], Set) :-
    mymember(H, Set),
    subset(T, Set).

union([], L, L).
union([H|T], L, R) :-
    mymember(H, L),
    union(T, L, R).
union([H|T], L, [H|R]) :-
    \+ mymember(H, L),
    union(T, L, R).

intersection([], _, []).
intersection([H|T], L, [H|R]) :-
    mymember(H, L),
    intersection(T, L, R).
intersection([H|T], L, R) :-
    \+ mymember(H, L),
    intersection(T, L, R).

difference([], _, []).
difference([H|T], L, R) :-
    mymember(H, L),
    difference(T, L, R).
difference([H|T], L, [H|R]) :-
    \+ mymember(H, L),
    difference(T, L, R).

equivalent(A, B) :-
    subset(A, B),
    subset(B, A).

% ---------- CARDINALITY ----------

cardinality([], 0).
cardinality([_|T], N) :-
    cardinality(T, N1),
    N is N1 + 1.

% ---------- MENU ----------

menu :-
    nl,
    write('----- SET OPERATIONS MENU -----'), nl,
    write('1. Member'), nl,
    write('2. Subset'), nl,
    write('3. Union'), nl,
    write('4. Intersection'), nl,
    write('5. Difference'), nl,
    write('6. Equivalent'), nl,
    write('7. Cardinality'), nl,
    write('8. Exit'), nl,
    loop.

% ---------- LOOP ----------

loop :-
    write('Enter your choice: '),
    read(Choice),
    process(Choice).

% ---------- PROCESS OPTIONS ----------

process(1) :-
    write('--- Member Check ---'), nl,
    write('Enter element: '), read(X),
    write('Enter list: '), read(L),
    (mymember(X, L) ->
        write('Element is a member')
    ;
        write('Element is NOT a member')
    ),
    nl, loop.

process(2) :-
    write('--- Subset Check ---'), nl,
    write('Enter subset list: '), read(A),
    write('Enter main list: '), read(B),
    (subset(A, B) ->
        write('It is a subset')
    ;
        write('Not a subset')
    ),
    nl, loop.

process(3) :-
    write('--- Union ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    union(A, B, R),
    write('Union = '), write(R), nl,
    loop.

process(4) :-
    write('--- Intersection ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    intersection(A, B, R),
    write('Intersection = '), write(R), nl,
    loop.

process(5) :-
    write('--- Difference ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    difference(A, B, R),
    write('Difference = '), write(R), nl,
    loop.

process(6) :-
    write('--- Equivalence Check ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    (equivalent(A, B) ->
        write('Sets are equivalent')
    ;
        write('Sets are NOT equivalent')
    ),
    nl, loop.

process(7) :-
    write('--- Cardinality ---'), nl,
    write('Enter list: '), read(L),
    cardinality(L, N),
    write('Cardinality = '), write(N), nl,
    loop.

process(8) :-
    write('Exiting program...'), nl.

process(_) :-
    write('Invalid choice! Try again.'), nl,
    loop.