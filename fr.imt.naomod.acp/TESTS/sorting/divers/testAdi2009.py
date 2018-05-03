# -------------------
# 29/4/2018
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

# 8 rules 
# subtyping
# 0: (Doctor(e) => Hospital(e)) 
#table.add_rule(doctor(h), hospital(h))
## 1: (Chief(e) => Hospital(e))  
#table.add_rule(chief(h), hospital(h))
## 2: (Nurse(e) => Hospital(e)) 
#table.add_rule(nurse(h), hospital(h)) 
# 3: (Hospital(e) => ~(Doctor(e) & Nurse(e))) 
#table.add_rule(hospital(h), Not(And(doctor(h), nurse(h))))
# 3:
#table.add_rule(And(doctor(h), nurse(h)), False) # other version ?
#table.add_rule(doctor(h), Not(nurse(h))) # 3bis
# 4: (![p,e] (doctor(e) => (Pread(e, p) & Pwrite(e, p))))
table.add_rule(doctor(h), And(pread(h, p), pwrite(h, p)))
# 5: (![d,p] ((doctor(d) & same(d, p)) => Pread(d, p)))
table.add_rule(And(doctor(h), sameward(h, p)), pread(h, p))
# 6: (![p,c] (chief(c) => Pread(c, p)))
table.add_rule(chief(h), pread(h, p))
# 7: (![n,p] ((nurse(h) & ~same(h, p)) => ~Pread(n, p)))
table.add_rule(And(nurse(h), Not(sameward(h, p))), Not(pread(h, p)))

#### ----------------
table.compute_table(4)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))
### print(str(table.get_safe_conditions()))

