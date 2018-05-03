# -------------------
# 3/5/2018
# Test Adi2009b
### exemple in motivation
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Patient = DeclareSort('Patient')
Hospital = DeclareSort('Hospital')

table = Sorting()
# Variables
table.add_variable("p", Patient)
table.add_variable("h", Hospital)
p = table.get_variable(0)
h = table.get_variable(1)
# more 
X= Const('X', Hospital)
toubib = Const('toubib', Hospital)
nounou = Const('nounou', Hospital)
bob = Const('bob', Patient)

# 4/1 + 3/2 predicates 
hospital = Function('hospital', Hospital, BoolSort()) 
doctor = Function('doctor', Hospital, BoolSort())     
nurse = Function('nurse', Hospital, BoolSort())
chief = Function('chief', Hospital, BoolSort())
pread = Function('pread', Hospital, Patient, BoolSort())
pwrite = Function('pwrite', Hospital, Patient, BoolSort())
sameward = Function('sameward', Hospital, Patient, BoolSort())

# 1: 
table.add_rule(And(doctor(h), nurse(h)), Not(sameward(h, p)))
#table.add_rule(And(nurse(h), doctor(h)), sameward(h, p))
# 2: 
table.add_rule(doctor(h), And(pread(h, p), pwrite(h, p)))
# 3: 
table.add_rule(And(doctor(h), sameward(h, p)), pread(h, p))
# 4: 
table.add_rule(chief(h), pread(h, p))
# 5: 
table.add_rule(And(nurse(h), Not(sameward(h, p))), Not(pread(h, p)))

#### =======================
table.compute_table(table.number_rule())
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))

