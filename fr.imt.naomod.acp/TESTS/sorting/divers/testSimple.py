# -------------------
# 17/12/2018
# Test simple ACP 
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Subject = DeclareSort('Subject')

table = Sorting()
# Variables
table.add_variable("X", Subject)
table.add_variable("P", IntSort())
X = table.get_variable(0)
P = table.get_variable(1)

known= Function('known', Subject, BoolSort()) 
password = Function('password', Subject, IntSort(), BoolSort())     
allow= Function('allow', Subject, BoolSort())

# the rules
table.add_rule(And(known(X), password(X, P)), allow(X))
#table.add_rule(Not(known(X)), Not(allow(X)))
#table.add_rule(And(known(X), Not(password(X, P))), Not(allow(X)))
table.add_rule(Or(known(X), Not(password(X, P))), Not(allow(X)))
#

### ===========================
size = 2
table.compute_table(size)
#table.check()
print (str(table))

