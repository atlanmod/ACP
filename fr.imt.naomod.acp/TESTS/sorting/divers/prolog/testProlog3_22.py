# -------------------
# 30/4/2018
# Test ArtOfProlog 
# -------------------
## Program 3.22: Quicksort
#     sort(Xs,Ys) :-  The list Ys is an ordered permutation of the list Xs.

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
List = DeclareSort('List')
Elem = DeclareSort('Elem')

table = Sorting()
# Variables
table.add_variable("X", Elem)
table.add_variable("Xs", List)
table.add_variable("Ys", List)
table.add_variable("Littles", List)
table.add_variable("Bigs", List)
table.add_variable("Ls", List)
table.add_variable("Bs", List)
table.add_variable("Y", Elem)
table.add_variable("Zs", List)

X = table.get_variable(0)
Xs = table.get_variable(1)
Ys = table.get_variable(2)
Littles = table.get_variable(3)
Bigs = table.get_variable(4)
Ls = table.get_variable(5)
Bs = table.get_variable(6)
Y = table.get_variable(7)
Zs = table.get_variable(8)

#  predicates 
quicksort = Function('quicksort', List, List, BoolSort()) 
partition = Function('partition', List, Elem, List, List, BoolSort()) 
append = Function('append', List, List, List, BoolSort()) 
cons = Function('cons', Elem, List, List) 
inf = Function('inf', Elem, Elem, BoolSort()) # X <= Y 

empty = Const('empty', List)

#     quicksort([],[]).
table.add_rule(True, quicksort(empty, empty))
 
#     quicksort([X|Xs],Ys) :-
#         partition(Xs,X,Littles,Bigs),
#         quicksort(Littles,Ls),
#         quicksort(Bigs,Bs),
#         append(Ls,[X|Bs],Ys).
table.add_rule(And(partition(Xs, X, Littles, Bigs), quicksort(Littles, Ls), quicksort(Bigs, Bs), append(Ls, cons(X, Bs),Ys)), quicksort(cons(X, Xs),Ys))
    
#     partition([],Y,[],[]).
table.add_rule(True, partition(empty, X, empty, empty))
#     partition([X|Xs],Y,[X|Ls],Bs) :- X =< Y, partition(Xs,Y,Ls,Bs).
table.add_rule(And(inf(X, Y), partition(Xs, Y, Ls, Bs)), partition(cons(X, Xs), Y, cons(X, Ls), Bs)) 
#     partition([X|Xs],Y,Ls,[X|Bs]) :- X >  Y, partition(Xs,Y,Ls,Bs).
table.add_rule(And(Not(inf(X, Y)), partition(Xs, Y, Ls, Bs)), partition(cons(X, Xs), Y, Ls, cons(X, Bs))) 

#     append([],Ys,Ys).
table.add_rule(True, append(empty, Ys, Ys))
#     append([X|Xs],Ys,[X|Zs]) :- append(Xs,Ys,Zs).
table.add_rule(append(Xs,Ys,Zs), append(cons(X, Xs), Ys, cons(X, Zs)))
### rules= 7 safe= 12 unsafe= 0 time= 1
### patine mais des unknow ? where is the problem ????
### le check <= patine ?

#### =====================
start = clock()
table.compute_table(7)
#table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str(floor(clock()-start)))
print (str(table))
### print(str(table.get_safe_conditions()))
#table.quine()
#table.perf("test")
