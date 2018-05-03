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

table.compute_table(3)
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
