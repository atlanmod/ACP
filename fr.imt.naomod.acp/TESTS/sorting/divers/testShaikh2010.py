# -------------------
# 22/4/2018
# test Table ...pour Shaikh2010
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# TODO analyse and explain pour l'instant rien de bon

#  sous-typage avec Z3 ?
# Administrator = DeclareSort('Administrator')
# Technician = DeclareSort('Technician')
# version sans sous-typage
Data = DeclareSort('Data')
Person = DeclareSort('Person')

root = Const('root', Person)
tech = Const('tech', Person)
data = Const('data', Data)

table = Sorting()
# Variables
table.add_variable("A", Person)
table.add_variable("C", Person)
table.add_variable("D", Data)
A = table.get_variable(0)
C = table.get_variable(1)
D = table.get_variable(2)

#  predicates 
rights = Function('rights', Person, Data, BoolSort()) 
pread = Function('pread', Person, Data, BoolSort()) 
pwrite = Function('pwrite', Person, Data, BoolSort()) 
pdelete = Function('pdelete', Person, Data, BoolSort()) 
person = Function('person', Person, BoolSort()) 
administrator = Function('administrator', Person, BoolSort()) 
technician = Function('technician', Person, BoolSort()) 
delegate = Function('delegate', Person, Person, BoolSort()) 

# RQ: ces 3 first rules y a une version equiv avec 2 rules sans le false
# (admin => (person & ~tech)) & (tech => (person & ~admin))
# subtyping 
#table.add_rule(administrator(A), person(A)) #0
#table.add_rule(technician(A), person(A))  #1
# # exclusive
table.add_rule(And(administrator(A), technician(A)), False) #2
# # rights
#table.add_rule(rights(A, D), And(pread(A, D), pwrite(A, D), pdelete(A, D))) #3
#table.add_rule(And(pread(A, D), pwrite(A, D), pdelete(A, D)), rights(A, D)) # 3bis
#table.add_rule(administrator(A), rights(A, D)) #4
table.add_rule(administrator(A), And(pread(A, D), pwrite(A, D), pdelete(A, D))) #3/4
table.add_rule(technician(C), And(pread(C, D), pwrite(C, D))) #5
#table.add_rule(And(administrator(A), technician(C), delegate(A, C)), rights(C, D)) #6
table.add_rule(And(administrator(A), technician(C), delegate(A, C)), And(pread(C, D), pwrite(C, D), pdelete(C, D))) #6/3
# # # delete only for administrators
table.add_rule(pdelete(A, D), administrator(A)) #7
#table.add_rule(technician(A), Not(pdelete(A, D))) #7bis

### 3/4 5 6 unsafe = 0
# FIX3_6
# ???

start = time()
table.compute_table(5) 
table.check()
# table.checkExclu()
# #table.checkSingleExclu()
# print ("time= " + str(time()-start))
print ("Table: " + str(table))
print ("safe= " + str(len(table.exclusive)) + " unsafe= " + str(len(table.unsafe))) 
# # safe= 4 unsafe= 10 without reverse of #3
# # safe= 4 unsafe= 5 with 
table.quine()


##### old stuff

### =============== 3-6
#  ----------- Sorted -------------- 
# <rights(A, D) => And(pread(A, D), pwrite(A, D), pdelete(A, D))>
# <administrator(A) => rights(A, D)>
# <technician(C) => And(pread(C, D), pwrite(C, D))>
# <And(administrator(A), technician(C), delegate(A, C)) => rights(C, D)>
#  ----------- Table -------------- 
# [1, 1, 1, 1] <[rights(A, D), administrator(A), technician(C), And(administrator(A), technician(C), delegate(A, C))] => [And(pread(A, D), pwrite(A, D), pdelete(A, D)), rights(A, D), And(pread(C, D), pwrite(C, D)), rights(C, D)]> SAT -- -- SAFE= --
# [1, 1, 1, 0] <[rights(A, D), administrator(A), technician(C), Not(And(administrator(A), technician(C), delegate(A, C)))] => [And(pread(A, D), pwrite(A, D), pdelete(A, D)), rights(A, D), And(pread(C, D), pwrite(C, D))]> SAT -- -- SAFE= --
# [1, 1, 0, 0] <[rights(A, D), administrator(A), Not(technician(C)), Not(And(administrator(A), technician(C), delegate(A, C)))] => [And(pread(A, D), pwrite(A, D), pdelete(A, D)), rights(A, D)]> SAT -- -- SAFE= --
# [1, 0, 1, 0] <[rights(A, D), Not(administrator(A)), technician(C), Not(And(administrator(A), technician(C), delegate(A, C)))] => [And(pread(A, D), pwrite(A, D), pdelete(A, D)), And(pread(C, D), pwrite(C, D))]> SAT -- -- SAFE= --
# [1, 0, 0, 0] <[rights(A, D), Not(administrator(A)), Not(technician(C)), Not(And(administrator(A), technician(C), delegate(A, C)))] => [And(pread(A, D), pwrite(A, D), pdelete(A, D))]> SAT -- -- SAFE= --
# [0, 0, 1, 0] <[Not(rights(A, D)), Not(administrator(A)), technician(C), Not(And(administrator(A), technician(C), delegate(A, C)))] => [And(pread(C, D), pwrite(C, D))]> SAT -- -- SAFE= --
#  ----------- Unsafe -------------- 
# [0, 1] <[Not(rights(A, D)), administrator(A)] => False> SAT unknown unknown SAFE= unknown
### DONC voit le PB et un fix possible FIX3-6
### peut demonstratif car stable
### +3bis ajoute pleins de unsafee idem +7

### =============== 3/4 + 5 + 3/6
### unsafe = 0
### +7 
#  ----------- Table -------------- 
# [1, 1, 1, -1] <[administrator(A), And(administrator(A), technician(C), delegate(A, C)), pdelete(A, D)] => [And(pread(A, D), pwrite(A, D), pdelete(A, D)), And(pread(C, D), pwrite(C, D), pdelete(C, D)), administrator(A)]> SAT -- -- SAFE= --
# [1, 0, 1, 1] <[administrator(A), Not(And(administrator(A), technician(C), delegate(A, C))), pdelete(A, D), technician(C)] => [And(pread(A, D), pwrite(A, D), pdelete(A, D)), administrator(A), And(pread(C, D), pwrite(C, D))]> SAT -- -- SAFE= --
# [1, 0, 1, 0] <[administrator(A), Not(And(administrator(A), technician(C), delegate(A, C))), pdelete(A, D), Not(technician(C))] => [And(pread(A, D), pwrite(A, D), pdelete(A, D)), administrator(A)]> SAT -- -- SAFE= --
# [0, 0, 0, 1] <[Not(administrator(A)), Not(And(administrator(A), technician(C), delegate(A, C))), Not(pdelete(A, D)), technician(C)] => [And(pread(C, D), pwrite(C, D))]> SAT -- -- SAFE= --
#  ----------- Unsafe -------------- 
# [1, 1, 0] <[administrator(A), And(administrator(A), technician(C), delegate(A, C)), Not(pdelete(A, D))] => False> SAT unknown unknown SAFE= unknown
# [1, 0, 0] <[administrator(A), Not(And(administrator(A), technician(C), delegate(A, C))), Not(pdelete(A, D))] => False> SAT unknown unknown SAFE= unknown
# [0, 0, 1] <[Not(administrator(A)), Not(And(administrator(A), technician(C), delegate(A, C))), pdelete(A, D)] => False> SAT unknown unknown SAFE= unknown
#### ??? obscure 
### version sans 5 et avec 7bis plus explicite et +2 similaire au cas Adi
