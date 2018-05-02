# -------------------
# 22/4/2018
# Test simple Person example
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Type = DeclareSort('Type')

table = Sorting()
# Variables
table.add_variable("X", Type)
X = table.get_variable(0)

student= Function('student', Type, BoolSort()) 
person = Function('person', Type, BoolSort())     
allow= Function('allow', Type, BoolSort())
other= Function('other', Type, BoolSort())

# table.add_rule(student(X), person(X))
# table.add_rule(student(X), allow(X))
# table.add_rule(person(X), Not(allow(X)))

# # # # 
# start = time()
# # # table.clean()
# table.compute_table(9, True)
# table.check() # 
# print ("time= " + str(time()-start))
# print ("Table: " + str(table))
# print ("safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
# ## quine
# #table.quine()
# 
# # Resultat
# #  ----------- Table -------------- 
# # [0, 0, 1] <[Not(student(X)), Not(student(X)), person(X)] => [Not(allow(X))]> SAT -- -- SAFE= --
# # 
# #  ----------- Unsafe -------------- 
# # [1, 1, 1] <[student(X), student(X), person(X)] => False> SAT unknown unknown SAFE= unknown
# # [1, 1, 0] <[student(X), student(X), Not(person(X))] => False> SAT unknown unknown SAFE= unknown
# # undefined = student(X)
# 
# # ### test safety
# # table.isSafe(ForAll(X, person(X))) # False
# # table.isSafe(ForAll(X, And(person(X), Not(student(X))))) # False
# # table.isSafe(ForAll(X, And(person(X), Not(allow(X)), Not(student(X))))) # True
# # table.isSafe(ForAll(X, And(person(X), Not(allow(X))))) # False
# # # a bit distrubing and not very intuitive because speaks about conclusions
# 
# # ### test isDefined should be better
# table.isDefined(ForAll(X, person(X))) # False
# table.isDefined(ForAll(X, student(X))) # False
# table.isDefined(ForAll(X, And(Not(student(X)), person(X)))) # True
# table.isDefined(ForAll(X, And(Not(student(X)), person(X), Not(allow(X))))) # True
# table.isDefined(ForAll(X, And(Not(student(X)), person(X), allow(X)))) # False
# # compute the set of max undefined 

# ### ===================== different example
### juste an obvious rule
# table.add_rule(student(X), False)
# table.add_rule(And(student(X), person(X)), allow(X))
# ### trouve bien le bon résultat 

# ### a bit diff
# table.add_rule(student(X), allow(X))
# table.add_rule(person(X), Not(allow(X)))
# table.add_rule(And(student(X), person(X)), other(X))
# # ### trouve bien le bon résultat car combinaison
## build = 8 resultat + simple au moins sur unsafe

# # ### a bit diff
# table.add_rule(And(student(X), person(X)), other(X))
# table.add_rule(student(X), allow(X))
# table.add_rule(person(X), Not(allow(X)))
# # # ### meme chose
# ###  build = 8 mais unsafe + complexe

### ===========================
table.compute_table(3)
table.check()
print (str(table))
table.quine()
#table.perf("test")

