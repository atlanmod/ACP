# -------------------
# 30/4/2018
# Test ArtOfProlog 
# -------------------
# %  Program 10.5    Unification algorithm
#    unify(Term1,Term2) :- 
#     Term1 and Term2 are unified, ignoring the occurs check.

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Term = DeclareSort('Term')
Funct = DeclareSort('Funct')

table = Sorting()
# Variables
table.add_variable("X", Term)
table.add_variable("Y", Term)
table.add_variable("N", IntSort())
table.add_variable("F", Funct)
table.add_variable("N1", IntSort())
table.add_variable("ArgX", Term)
table.add_variable("ArgY", Term)

X = table.get_variable(0)
Y = table.get_variable(1)
N = table.get_variable(2)
F = table.get_variable(3)
N1 = table.get_variable(4)
ArgX = table.get_variable(5)
ArgY = table.get_variable(6)

#  predicates 
unify = Function('unify', Term, Term, BoolSort()) 
nonvar = Function('nonvar', Term, BoolSort()) 
var = Function('var', Term, BoolSort()) 
constant = Function('constant', Term, BoolSort()) 
compound = Function('compound', Term, BoolSort()) 
term_unify = Function('term_unify', Term, Term, BoolSort()) 
functor = Function('functor', Term, Funct, IntSort(), BoolSort()) 
unify_args = Function('unify_args', IntSort(), Term, Term, BoolSort()) 
unify_arg = Function('unify_arg', IntSort(), Term, Term, BoolSort()) 
arg = Function('arg', IntSort(), Term, Term, BoolSort()) 

#    unify(X,Y) :- var(X), var(Y), X=Y.
table.add_rule(And(var(X), var(Y), X==Y), unify(X, Y))
#    unify(X,Y) :- var(X), nonvar(Y), X=Y.
table.add_rule(And(var(X), nonvar(Y), X==Y), unify(X, Y))
#    unify(X,Y) :- var(Y), nonvar(X), Y=X.
table.add_rule(And(var(Y), nonvar(X), X==Y), unify(X, Y))
#    unify(X,Y) :- nonvar(X), nonvar(Y), constant(X), constant(Y), X=Y.
table.add_rule(And(nonvar(Y), nonvar(X), constant(X), constant(Y), X==Y), unify(X, Y))
#    unify(X,Y) :- nonvar(X), nonvar(Y), compound(X), compound(Y), term_unify(X,Y).
table.add_rule(And(nonvar(Y), nonvar(X), compound(X), compound(Y)), unify(X, Y))
#    term_unify(X,Y) :- functor(X,F,N), functor(Y,F,N), unify_args(N,X,Y).
table.add_rule(And(functor(X, F, N), functor(Y, F, N), unify_args(N, X, Y)), term_unify(X, Y))
#    unify_args(N,X,Y) :- N > 0, unify_arg(N,X,Y), N1 is N-1, unify_args(N1,X,Y).
table.add_rule(And(N>0, N1==N-1, unify_arg(N, X, Y)), unify_args(N1, X, Y)), 
#    unify_args(0,X,Y).
table.add_rule(N==0, unify_args(N, X, Y))
#    unify_arg(N,X,Y) :- arg(N,X,ArgX), arg(N,Y,ArgY), unify(ArgX,ArgY).
table.add_rule(And(arg(N, X, ArgX), arg(N, Y, ArgY)), unify_arg(N, X, Y))

### TODO check it and see version with occur check
### rules= 9 safe= 47 unsafe= 0 time= 3 but there are build unknown ...

#### =====================
start = clock()
table.compute_table(9)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str(floor(clock()-start)))
print (str(table))
### print(str(table.get_safe_conditions()))
#table.quine()
#table.perf("test")
