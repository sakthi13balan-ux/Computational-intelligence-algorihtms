run:-
    write('---Menu---'),nl,
    write('1-Addition'),nl,
    write('2-Subtraction'),nl,
    write('3-Multiplication'),nl,
    write('4-Division'),nl,
    write('5-Modulus'),nl,
    write('6-Exit'),nl,
    loop.

loop:-
    write('Enter your choice:'),
    read(Choice),nl,
    process_calculator(Choice).

read_input(A,B):-
   write('Enter the first number:'),
   read(A),nl,
   write('Enter the second number:'),
   read(B),nl.

process_calculator(1):-
    read_input(A,B),
    calculate(+,A,B,Result),
    write('Result: '),write(A),write('+'),write(B),write('='),write(Result),nl,
    loop.
process_calculator(2):-
    read_input(A,B),
    calculate(-,A,B,Result),
    write('Result: '),write(A),write('-'),write(B),write('='),write(Result),nl,
    loop.
process_calculator(3):-
    read_input(A,B),
    calculate(*,A,B,Result),
    write('Result: '),write(A),write('*'),write(B),write('='),write(Result),nl,
    loop.
process_calculator(4):-
    read_input(A,B),
    calculate(/,A,B,Result),
    write('Result: '),write(A),write('/'),write(B),write('='),write(Result),nl,
    loop.
process_calculator(5):-
    read_input(A,B),
    calculate(mod,A,B,Result),
    write('Result: '),write(A),write('mod'),write(B),write('='),write(Result),nl,
    loop.
process_calculator(6):-
    write('---END---'),nl.

process_calculator(_):-
    write('---INVALID OPTION---'),nl,
    loop.

calculate(+,A,B,Result):-
    Result is A+B.
calculate(-,A,B,Result):-
    Result is A-B.
calculate(*,A,B,Result):-
    Result is A*B.
calculate(/,A,B,Result):-
    (B=:=0 -> write('Divide by zero error'),nl,Result is inf;
    Result is A/B),nl.
calculate(mod,A,B,Result):-
    (B=:=0 -> write('Divide by zero error'),nl,Result is inf;
    Result is A mod B),nl.








