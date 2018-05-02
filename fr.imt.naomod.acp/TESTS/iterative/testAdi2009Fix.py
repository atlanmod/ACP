# -------------------
# 16/4/2018
# Test Adi2009 
# -------------------

from Iterative import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Patient = DeclareSort('Patient')
Hospital = DeclareSort('Hospital')

table = Iterative()
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

# # # # original rules 
#table.add_rule(Or(doctor(h), chief(h), nurse(h)), hospital(h)) #1
#table.add_rule(hospital(h), Or(doctor(h), chief(h), nurse(h))) #2
# # # # # # # #
table.add_rule(And(doctor(h), nurse(h)), False) #3
# # # table.add_rule(And(chief(h), nurse(h)), False) #4
# # # table.add_rule(And(doctor(h), chief(h)), False) #5
# # # # # # # # # # #
table.add_rule(doctor(h), And(pread(h, p), pwrite(h, p))) #6
#table.add_rule(chief(h), pread(h, p))  #7
table.add_rule(And(nurse(h), Not(sameward(h, p))), Not(pread(h, p))) #8
table.add_rule(And(chief(h), sameward(h, p)), pread(h, p)) #9

# modif of 6+8+9 
##table.add_rule(doctor(h), And(pread(h, p), pwrite(h, p))) #6
# table.add_rule(And(doctor(h), sameward(h, p)), And(pread(h, p), pwrite(h, p))) #6new
# table.add_rule(And(nurse(h), Not(sameward(h, p))), Not(pread(h, p))) #8
# table.add_rule(And(chief(h), sameward(h, p)), pread(h, p)) #9
# 
# # # 
# start = time()
# # # table.clean()
# table.compute_table(9, True)
# table.check() # 
# print ("time= " + str(time()-start))
# print ("Table: " + str(table))
# print ("safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
# ## quine
# #table.quine()

table.compute_table(4)
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))
