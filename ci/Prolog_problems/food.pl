likes(ravi,X) :- food(X).
food(apple).
food(chicken).
food(Y) :- eats(X,Y), \+ killed(X).
eats(ajay, peanut).
alive(ajay).
eats(rita,X) :- eats(ajay,X).
alive(X):- \+killed(X).
killed(X):- \+alive(X).