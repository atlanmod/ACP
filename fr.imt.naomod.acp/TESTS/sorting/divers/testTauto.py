# -------------------
# 17/5/2018
# Test tautology 
# -------------------

#from Improve import * #@UnusedWildImport
from Sorting import * #@UnusedWildImport
#from Iterative import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
#table = Iterative()
table = Sorting()
# Variables
table.add_variable("X", IntSort()) ## TODO fix it
A = Const('A', BoolSort())
B = Const('B', BoolSort())
C = Const('C', BoolSort())
D = Const('D', BoolSort())
E = Const('E', BoolSort())
F = Const('F', BoolSort())
G = Const('G', BoolSort())
H = Const('H', BoolSort())

# removed before
###table.add_rule(A, A)

# #### cas <= sat 1 tauto 2 unsafe may be pb lastNot
# table.add_rule(A, B)
# table.add_rule(B, A)
# table.add_rule(C, D)
#table.add_rule(E, F)

# # #### cas chaining == similaire au pred
# table.add_rule(A, B)
# table.add_rule(B, C)
# table.add_rule(C, A)
# table.add_rule(D, E)

### with 2 tauto at least
# table.add_rule(A, B)
# table.add_rule(B, A)
# table.add_rule(C, D)
# table.add_rule(E, F)
# table.add_rule(C, G)
# table.add_rule(F, E)

#----------------------------------
# # example with inclusion condition 
# table.add_rule(And(B, A), C)
# table.add_rule(A, B)
# #table.add_rule(C, D)
# table.add_rule(Or(E, A, B), F)
# # table.add_rule(C, G)
# # table.add_rule(F, E)

#----------------------------------
# test SMER ?
table.add_rule(And(B, A), False)
table.add_rule(C, A)
table.add_rule(D, B)
# but first is eliminated by clean 
# but Enumerative.clean not correct ???
#----------------------------------

### ===============
table.compute_table(3)
table.check()
print ("rules= " + str(len(table.rules)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))
# ### print(str(table.get_safe_conditions()))
# #table.quine()
# #table.perf("test")

# ### -------------
# table.clean(6)
# for r in table.correct:
#     print(str(r))
# table.cond_inclusions()
