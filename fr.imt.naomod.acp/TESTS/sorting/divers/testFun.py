# -------------------
# 3/5/2018
# Test simple computation
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
#Type = DeclareSort('Type')

table = Sorting()
# Variables
table.add_variable("I", IntSort())
table.add_variable("J", IntSort())
#table.add_variable("K", IntSort())
I = table.get_variable(0)
J = table.get_variable(1)
#K = table.get_variable(2)

### predicates
fun= Function('fun', IntSort(), IntSort()) 
H= Function('H', IntSort(), IntSort(), IntSort()) 
G= Function('G', IntSort(),  IntSort()) 
fact= Function('fact', IntSort(), IntSort()) 

### R1
# table.add_rule((I <= 3), fun(I) == I-2)
# table.add_rule((I >= 1), fun(I) == I+1)

### R2
# table.add_rule((I == 0), H(I, J) == I)
# table.add_rule((J == 0), H(I, J) == J)
# table.add_rule((I <= J), H(I, J) == J-I)
# table.add_rule((I >= J), H(I, J) == J+I)

### R3
table.add_rule((I == 0), fact(I) == 1)
table.add_rule((I == 1), fact(I) == 1)
table.add_rule((I == 2), fact(I) == 1)
table.add_rule((I >= 1), fact(I) == I * fact(I-1))

# ### R4
# table.add_rule((I >= 0), H(I, J) == I)
# table.add_rule((J >= 0), H(I, J) == J)
# table.add_rule((I <= J), H(I, J) == G(I+J))
# table.add_rule((I >= J), H(I, J) == J+I)
# table.add_rule(True, G(I) == I+2)
### there are unknwon satisfiability result but proceed 

### ===========================
table.compute_table(table.number_rule())
table.check()
print (str(table))

