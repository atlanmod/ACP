# -------------------
# 17/4/2018
# Test simple Person example
# -------------------

### need to include the algorithm you want
###  (Enumerative, Iterative, or Sorting)
from Iterative import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
### use Z3 to declare some sort or use the primitive one from Z3
Type = DeclareSort('Type')

### define your table (Enumerative, Iterative, or Sorting)
table = Iterative()
# add variables in two steps
table.add_variable("X", Type)
table.add_variable("Y", IntSort())
### ordering matters ...
X = table.get_variable(0)
Y = table.get_variable(1)

#### declare your functions/predicates as usual in Z3
student= Function('student', Type, BoolSort()) 
person = Function('person', Type, BoolSort())     
allow= Function('allow', Type, BoolSort())

#### you rules in the table, it is a pair of Z3 expressions
table.add_rule(student(X), person(X))
table.add_rule(student(X), allow(X))
table.add_rule(person(X), Not(allow(X)))

### call the algorithm, 
### the numeric parameter is for stopping the analysis to the first rules 
table.compute_table(table.number_rule())
### some results
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))