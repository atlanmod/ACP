# -------------------
# 27/4/2018
# Test Fatema2012 analyse of old GDPR
# Table 1 natural ACR (but CRR ?)
# -------------------

### TODO reread the explanation

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Person = DeclareSort('Person')
Data = DeclareSort('Data')
Purpose = DeclareSort('Purpose')
Message = DeclareSort('Message')

table = Sorting()
# Variables
table.add_variable("X", Person)
table.add_variable("Y", Data)
table.add_variable("Z", Purpose)
table.add_variable("T", IntSort()) ### time 
table.add_variable("M", Message) 
table.add_variable("Xr", Person) ### requester
X = table.get_variable(0)
Y = table.get_variable(1)
Z = table.get_variable(2)
T = table.get_variable(3)
M = table.get_variable(4)
Xr = table.get_variable(5)
# more 
# update data request
UDR= Const('UDR', Message)

# predicates 
anyone = Function('anyone', Person, BoolSort()) 
data = Function('data', Data, BoolSort()) 
personal = Function('personal', Data, BoolSort()) 
purpose = Function('purpose', Purpose, BoolSort()) 
# of data collection/ historical purpose/statistical purpose / scientific purpose
legal = Function('legal', Purpose, BoolSort()) 
# data subject and owned the data
subject = Function('subject', Person, Data, BoolSort()) 
log = Function('log', Message, Person, Data, BoolSort()) 
inaccurate = Function('inaccurate', Data, BoolSort()) 
# performance of contract
performance = Function('performance', Data, BoolSort()) 
contract = Function('contract', Person, Person, Data, BoolSort()) 
specific_role = Function('specific_role', Person, BoolSort()) 
specific = Function('specific', Data, BoolSort()) 
official = Function('official', Purpose, BoolSort()) 
# access mandate ?
access = Function('access', Person, Data, BoolSort()) 
#
legal_objection = Function('legal_objection', Data, BoolSort()) 

PREAD = Function('PREAD', Person, Data, BoolSort())
PWRITE = Function('PREAD', Person, Data, BoolSort())
### 
PUPDATE = Function('PUPDATE', Person, Data, BoolSort()) 
# submit and update policy
PSUBPOL = Function('PSUBPOL', Person, Data, BoolSort()) 

### TODO revoir personal => data
### TODO add time parameter ? donc ajout dans l'action ?

### ============= rules
### R1
table.add_rule(personal(Y), data(Y))
table.add_rule(legal(Z), purpose(Z))
### but ? OR validity time earlier than the requested time.
table.add_rule(And(anyone(X), personal(Y), purpose(Z), Not(legal(Z))), Not(PREAD(X, Y)))
### R2
table.add_rule(inaccurate(Y), data(Y))
table.add_rule(And(subject(X, Y), personal(Y), inaccurate(Y)), And(PUPDATE(X, Y), log(UDR, X, Y)))
# # ### R3
table.add_rule(And(subject(X, Y), personal(Y)), PSUBPOL(X, Y))
# ### R4
table.add_rule(performance(Y), data(Y))
#table.add_rule(And(subject(X, Y), personal(Y), performance(Y), contract(X, Xr, Y)), And(PREAD(X, Y), PWRITE(X, Y)))
# ### => introduit 2 unsafe [0, 1, 1, 1, 1] [0, 1, 0, 1, 1]
# ### why ? Not(legal(Z))
# ### solution ?  add legal(Z) dans R4
table.add_rule(And(subject(X, Y), personal(Y), performance(Y), contract(X, Xr, Y), legal(Z)), And(PREAD(X, Y), PWRITE(X, Y)))
# #### no unsafe ----------
# ### R5
table.add_rule(specific(Y), data(Y))
table.add_rule(official(Z), purpose(Z))
#table.add_rule(And(subject(X, Y), specific_role(X), specific(Y), official(Z)), PREAD(X, Y)) 
## rules= 11 safe= 38 unsafe= 2 time 3.5
# #  [1, 1, 1, 0, 1, 0, 1] [1, 0, 1, 0, 1, 0, 1]
table.add_rule(And(subject(X, Y), specific_role(X), specific(Y), official(Z), legal(Z)), PREAD(X, Y)) 
#rules= 11 safe= 33 unsafe= 0 time 3.271161
# ### R6 
###table.add_rule(And(subject(X, Y), personal(Y), access(X, Y)), And(PREAD(X, Y), PWRITE(X, Y), PUPDATE(X, Y))) 
#     rules= 12 safe= 39 unsafe= 2 time 3.8
###  [1, 1, 1, 1] [1, 0, 1, 1] meme pb
table.add_rule(And(subject(X, Y), personal(Y), access(X, Y), legal(Z)), And(PREAD(X, Y), PWRITE(X, Y), PUPDATE(X, Y))) 
## rules= 12 safe= 35 unsafe= 0 time 3.7
### R7 two rules indeed
table.add_rule(And(subject(X, Y), personal(Y), legal_objection(Y)), Not(PREAD(X, Y)))
#table.add_rule(And(subject(X, Y), personal(Y), Not(legal_objection(Y))), PREAD(X, Y))
### une seule rule rules= 13 safe= 41 unsafe= 6 time 4.8
### suspicious legal_objecttion manque dans autre PREAD
### les 2 rules= 14 safe= 41 unsafe= 10 time 5.793029

#### ======================
start = clock()
table.compute_table(13)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time " + str(clock()-start))
print (str(table))
#table.quine()
