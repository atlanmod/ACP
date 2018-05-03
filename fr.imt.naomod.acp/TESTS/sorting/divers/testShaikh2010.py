# -------------------
# 22/4/2018
# test Shaikh2010
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

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

start = time()
table.compute_table(5) 
table.check()
# table.checkExclu()
# #table.checkSingleExclu()
# print ("time= " + str(time()-start))
print ("Table: " + str(table))
print ("safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe))) 
