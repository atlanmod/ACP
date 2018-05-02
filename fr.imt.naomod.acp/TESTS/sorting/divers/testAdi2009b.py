# -------------------
# 230/4/2018
# Test Adi2009 
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

### with that And(doctor(h), nurse(h)) => false 
## table.add_rule(And(doctor(h), nurse(h)), False)

#### =======================
table.compute_table(6)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))
# print(str(table.tspass(table.rules)))
# print(str(table.tspass(table.safe)))
# print(str(table.tspass(table.unsafe)))
#table.quine()
#table.perf("test")
