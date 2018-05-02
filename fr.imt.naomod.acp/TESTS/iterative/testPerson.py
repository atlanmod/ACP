# -------------------
# 17/4/2018
# Test simple Person example
# -------------------

from Iterative import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Type = DeclareSort('Type')

table = Iterative()
# Variables
table.add_variable("X", Type)
X = table.get_variable(0)

student= Function('student', Type, BoolSort()) 
person = Function('person', Type, BoolSort())     
allow= Function('allow', Type, BoolSort())

table.add_rule(student(X), person(X))
table.add_rule(student(X), allow(X))
table.add_rule(person(X), Not(allow(X)))

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

# Resultat
#  ----------- Table -------------- 
# [0, 0, 1] <[Not(student(X)), Not(student(X)), person(X)] => [Not(allow(X))]> SAT -- -- SAFE= --
# 
#  ----------- Unsafe -------------- 
# [1, 1, 1] <[student(X), student(X), person(X)] => False> SAT unknown unknown SAFE= unknown
# [1, 1, 0] <[student(X), student(X), Not(person(X))] => False> SAT unknown unknown SAFE= unknown
# undefined = student(X)

### test safety
# table.isSafe(ForAll(X, person(X))) # sat
# table.isSafe(ForAll(X, And(person(X), Not(student(X))))) # sat
# table.isSafe(ForAll(X, And(person(X), Not(allow(X)), Not(student(X))))) # unsat
# table.isSafe(ForAll(X, And(person(X), Not(allow(X))))) # sat
# un peu perturbant cela ... car j'ai la réponse !!!!

### test isDefined should be sat
#table.isDefined(ForAll(X, person(X))) # sat OK
#table.isDefined(ForAll(X, student(X))) # unsat NOK
#table.isSafe(ForAll(X, And(person(X), Not(student(X))))) # sat OK

table.compute_table(3)
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
