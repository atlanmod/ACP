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

table.add_rule(student(X), person(X))
table.add_rule(student(X), allow(X))
table.add_rule(person(X), Not(allow(X)))

### ===========================
table.compute_table(3)
table.check()
print (str(table))

