# -------------------
# 29/4/2018
# Test Adi2009 
# -------------------

### May be aligned with the original
### and show that we find more errors and more precise
### Note also that it suggest some fixes: adding unsafe, adding conditions, desactivating rules

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
# 3: plutot
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

# FIX1
#table.add_rule(And(nurse(h), chief(h)), False)
#table.add_rule(And(doctor(h), chief(h)), False)

# # # 
# start = time()
# table.compute_table(10, False)
# table.check() # 
# table.checkExclu()
# table.checkSingleExclu()
# print ("time= " + str(time()-start))
# print ("Table: " + str(table))
# print ("safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe))) 
# 
# ### we can illustrate that more complete and more precise than original example
# ### suggestion to fix 
# 
# # #### 3-7
# # ### 
# # table.isSafe(ForAll([h, p], And(Not(doctor(h)), nurse(h), Not(sameward(h, p)), chief(h)))) # sat thus a problem
# # table.isSafe(ForAll(h, And(doctor(h), nurse(h))))  # sat thus a problem
# # # 
# # table.isDefined(ForAll([h, p], Or(doctor(h), nurse(h), chief(h)))) # False
# # table.isDefined(ForAll([h, p], Or(doctor(h), Not(nurse(h)), chief(h)))) # False
# # table.isDefined(ForAll([h, p], And(doctor(h), Not(nurse(h)), sameward(h, p)))) # True (match first)
# # table.isDefined(ForAll([h, p], And(doctor(h), Not(nurse(h))))) # True (1st)
# # table.isDefined(ForAll([h, p], And(Not(doctor(h)), nurse(h), Not(sameward(h, p)), Not(chief(h))))) # True (2nd)
# # table.isDefined(ForAll([h, p], And(Not(doctor(h)), Not(nurse(h)), Not(sameward(h, p)), chief(h)))) # True (3nd)
# # ### 
# 
# #### 3bis-7
# #  ----------- Safe -------------- 
# # SAFE [1, 1, 0, -1, -1] <[doctor(h), doctor(h), Not(And(nurse(h), Not(sameward(h, p))))] => [Not(nurse(h)), And(pread(h, p), pwrite(h, p))]>
# # SAFE [0, 0, 1, 0, 0] <[Not(doctor(h)), Not(doctor(h)), And(nurse(h), Not(sameward(h, p))), Not(And(doctor(h), sameward(h, p))), Not(chief(h))] => [Not(pread(h, p))]>
# # SAFE [0, 0, 0, 0, 1] <[Not(doctor(h)), Not(doctor(h)), Not(And(nurse(h), Not(sameward(h, p)))), Not(And(doctor(h), sameward(h, p))), chief(h)] => [pread(h, p)]>
# #  ----------- Unsafe -------------- 
# # UNSAFE [1, 1, 1] <[doctor(h), doctor(h), And(nurse(h), Not(sameward(h, p)))] => False>
# # UNSAFE [0, 0, 1, 0, 1] <[Not(doctor(h)), Not(doctor(h)), And(nurse(h), Not(sameward(h, p))), Not(And(doctor(h), sameward(h, p))), chief(h)] => False>
# ### which should be after manual simplification (complex, expensive, impact of rules ?)
# #  ----------- Safe -------------- 
# # [doctor(h), Not(And(nurse(h), Not(sameward(h, p)))] => [Not(nurse(h)), And(pread(h, p), pwrite(h, p))]
# # [Not(doctor(h)), And(nurse(h), Not(sameward(h, p))), Not(chief(h))] => [Not(pread(h, p))]
# # [Not(doctor(h)), Not(nurse(h)), chief(h)] => [pread(h, p)]
# # [Not(doctor(h)), Not(nurse(h)), Not(sameward(h, p)), chief(h)] => [pread(h, p)]
# # [Not(doctor(h)), sameward(h, p),  chief(h)] => [pread(h, p)]
# #  ----------- Unsafe -------------- 
# # [doctor(h), nurse(h), Not(sameward(h, p))] => False
# # [Not(doctor(h)), nurse(h), Not(sameward(h, p)), chief(h)] => False>
# ### TODO check equiv
# # print(str(table.tspass(table.rules)))
# # print(str(table.z3_safe()))
# 
# ## 
# table.isDefined(ForAll([h, p], Or(doctor(h), nurse(h), chief(h)))) # False
# table.isDefined(ForAll([h, p], Or(doctor(h), Not(nurse(h)), chief(h)))) # False
# table.isDefined(ForAll([h, p], And(doctor(h), Not(nurse(h)), sameward(h, p)))) # True (match first)
# table.isDefined(ForAll([h, p], And(doctor(h), Not(nurse(h))))) # True (1st)
# table.isDefined(ForAll([h, p], And(Not(doctor(h)), nurse(h), Not(sameward(h, p)), Not(chief(h))))) # True (2nd)
# table.isDefined(ForAll([h, p], And(Not(doctor(h)), Not(nurse(h)), Not(sameward(h, p)), chief(h)))) # True (3nd)
# ### compute TODO maxDefined

#### union of safe conditions
# print (str(tactic(ForAll([h, p], Or(And(doctor(h), doctor(h), Not(And(nurse(h), Not(sameward(h, p))))),
#                 And(Not(doctor(h)), Not(doctor(h)), And(nurse(h), Not(sameward(h, p))), Not(And(doctor(h), sameward(h, p))), Not(chief(h))),
#     And(Not(doctor(h)),
#                 Not(doctor(h)),
#                 Not(And(nurse(h), Not(sameward(h, p)))),
#                 Not(And(doctor(h), sameward(h, p))),
#                 chief(h)))))))
### simplif ???
# ForAll([h, p],
#          Or(And(doctor(h),
#                 Or(Not(nurse(h)), sameward(h, p))),
#             And(Not(doctor(h)),
#                 nurse(h),
#                 Not(sameward(h, p)),
#                 Or(Not(doctor(h)), Not(sameward(h, p))),
#                 Not(chief(h))),
#             And(Not(doctor(h)),
#                 Or(Not(nurse(h)), sameward(h, p)),
#                 Or(Not(doctor(h)), Not(sameward(h, p))),
#                 chief(h))))

#### ------------ 4-7

table.compute_table(4)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))
### print(str(table.get_safe_conditions()))
#table.quine()
#table.perf("test")
