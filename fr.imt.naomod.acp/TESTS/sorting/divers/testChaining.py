# -------------------
# 24/4/2018
# Test simple chaining propositionnal
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Type = DeclareSort('Type')

table = Sorting()
# # Variables
table.add_variable("X", Type)
X = table.get_variable(0)


P0 = Const('P0', BoolSort())
D1 = Const('D1', BoolSort())
C1 = Const('C1', BoolSort())
D2 = Const('D2', BoolSort())
C2 = Const('C2', BoolSort())
# 
# table.add_rule(D1, C1)
# table.add_rule(C1, C2)
# table.add_rule(C2, Not(D1))

#### ===============
#  ----------- Safe -------------- 
# SAFE [0, 1, 1] <[Not(D1), C1, C2] => [C2, Not(D1)]>
# SAFE [0, 0, 1] <[Not(D1), Not(C1), C2] => [Not(D1)]>
#  ----------- Unsafe -------------- 
# UNSAFE [1, 0] <[D1, Not(C1)] => False>
# UNSAFE [1, 1, 1] <[D1, C1, C2] => False>
# UNSAFE [1, 1, 0] <[D1, C1, Not(C2)] => False>
# UNSAFE [0, 1, 0] <[Not(D1), C1, Not(C2)] => False>
# 
# quine listbin [[1, 0], [1, 1, 1], [1, 1, 0], [0, 1, 0]]
# allmins [[1, 0, 0], [1, 0, 1], [1, 1, 1], [1, 1, 0], [0, 1, 0]]
# Quine= Or(And(C1, Not(C2)), And(D1))
# +tactic= [[C1, Not(C2)], [D1]]

# ### TODO trouver un exemple plus intéresant avec variables
# student= Function('student', Type, BoolSort()) 
# professor= Function('professor', Type, BoolSort())     
# doctorant = Function('doctorant', Type, BoolSort())
# isTeaching= Function('isTeaching', Type, BoolSort())
# 
# table.add_rule(student(X), Not(isTeaching(X)))
# table.add_rule(professor(X), isTeaching(X))
# table.add_rule(doctorant(X), And(student(X), professor(X)))

#  ----------- Safe -------------- 
# SAFE [1, 0, 0] <[student(X), Not(professor(X)), Not(doctorant(X))] => [Not(isTeaching(X))]>
# SAFE [0, 1, 0] <[Not(student(X)), professor(X), Not(doctorant(X))] => [isTeaching(X)]>
#  ----------- Unsafe -------------- 
# UNSAFE [1, 1] <[student(X), professor(X)] => False>
# UNSAFE [1, 0, 1] <[student(X), Not(professor(X)), doctorant(X)] => False>
# UNSAFE [0, 1, 1] <[Not(student(X)), professor(X), doctorant(X)] => False>
# UNSAFE [0, 0, 1] <[Not(student(X)), Not(professor(X)), doctorant(X)] => False>
# 
# Quine= Or(And(student(X), professor(X)), And(doctorant(X)))
# +tactic= [[student(X), professor(X)], [doctorant(X)]]

#### example with unsat core not minimal
#table.add_rule(D1, C1)
table.add_rule(And(D1, D2), C2)
table.add_rule(C2, P0)
table.add_rule(D1, Not(P0))

#### with only 3 last rules
#  ----------- Safe -------------- 
# SAFE [0, 1, 0] <[Not(And(D1, D2)), C2, Not(D1)] => [P0]>
# SAFE [0, 0, 1] <[Not(And(D1, D2)), Not(C2), D1] => [Not(P0)]>
#  ----------- Unsafe -------------- 
# UNSAFE [1, 0] <[And(D1, D2), Not(C2)] => False>
# UNSAFE [1, 1, 1] <[And(D1, D2), C2, D1] => False>
# UNSAFE [0, 1, 1] <[Not(And(D1, D2)), C2, D1] => False>

#### with the 4 rules
#  ----------- Safe -------------- 
# SAFE [1, 0, 0, 1] <[D1, Not(And(D1, D2)), Not(C2), D1] => [C1, Not(P0)]>
# SAFE [0, 0, 1, 0] <[Not(D1), Not(And(D1, D2)), C2, Not(D1)] => [P0]>
#  ----------- Unsafe -------------- 
# UNSAFE [1, 1, 0] <[D1, And(D1, D2), Not(C2)] => False>
# UNSAFE [1, 1, 1, 1] <[D1, And(D1, D2), C2, D1] => False>
# UNSAFE [1, 0, 1, 1] <[D1, Not(And(D1, D2)), C2, D1] => False>


### ===========================
# table.compute_table(3)
table.compute_table(3)
table.check()
print (str(table))
#table.quine()

