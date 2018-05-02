# -------------------
# 29/4/2018
# Test Fatema2012 analyse of old GDPR
# Table 1 natural ACR (but CRR ?)
# -------------------
### fix legal_objection dans Not PREAD and vice-versa

### TODO reread the explanation
### they forget implication/subsort inequalities, 

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
# 
medical = Function('medical', Data, BoolSort()) 
doctor = Function('doctor', Person, Person, BoolSort()) 
diagnosis = Function('diagnosis', Purpose, BoolSort()) 

PREAD = Function('PREAD', Person, Data, BoolSort())
PWRITE = Function('PWRITE', Person, Data, BoolSort())
### 
PUPDATE = Function('PUPDATE', Person, Data, BoolSort()) 
# submit and update policy
PSUBPOL = Function('PSUBPOL', Person, Data, BoolSort()) 
# +transfer

### TODO revoir personal => data
### TODO add time parameter ? donc ajout dans l'action ?

### ============= rules
### R1
table.add_rule(personal(Y), data(Y))
table.add_rule(legal(Z), purpose(Z))
### but ? OR validity time earlier than the requested time.
table.add_rule(And(anyone(X), personal(Y), purpose(Z), Not(legal(Z)), legal_objection(Y)), Not(PREAD(X, Y)))
# ### R2
table.add_rule(inaccurate(Y), data(Y))
table.add_rule(And(subject(X, Y), personal(Y), inaccurate(Y)), And(PUPDATE(X, Y), log(UDR, X, Y)))
# # # ### R3
table.add_rule(And(subject(X, Y), personal(Y)), PSUBPOL(X, Y))
# ### R4 !!! here Xr is the requester
table.add_rule(performance(Y), data(Y))
table.add_rule(And(subject(X, Y), personal(Y), performance(Y), contract(X, Xr, Y)), And(PREAD(Xr, Y), PWRITE(Xr, Y)))
### rules= 8 safe= 20 unsafe= 0 time 1.6
# # ### R5
table.add_rule(specific(Y), data(Y))
#### table.add_rule(official(Z), purpose(Z))
table.add_rule(legal(Z), official(Z)) ### correctif R8+doctor
# table.add_rule(And(subject(X, Y), specific_role(X), specific(Y), official(Z)), PREAD(X, Y)) 
## rules= 11 safe= 50 unsafe= 4 time 4.1
# # [1, 1, 1, 1, 1] ... 
table.add_rule(And(subject(X, Y), specific_role(X), specific(Y), official(Z), legal(Z), Not(legal_objection(Y))), PREAD(X, Y)) 
# # rules= 11 safe= 43 unsafe= 0 time 3.7
# # ### R6 
#table.add_rule(And(subject(X, Y), personal(Y), access(X, Y)), And(PREAD(X, Y), PWRITE(X, Y), PUPDATE(X, Y))) 
# # rules= 12 safe= 55 unsafe= 4 time 4.9
# ###  [1, 1, 1, 1] same 
table.add_rule(And(subject(X, Y), personal(Y), access(X, Y), legal(Z), Not(legal_objection(Y))), And(PREAD(X, Y), PWRITE(X, Y), PUPDATE(X, Y))) 
# ## rules= 12 safe= 47 unsafe= 0 time 4.477334
### R7 two rules indeed
table.add_rule(And(subject(X, Y), personal(Y), legal_objection(Y)), Not(PREAD(X, Y)))
# rules= 13 safe= 59 unsafe= 0 time 5.6
# ### one rule OLD fox 
# ### suspicious legal_objection lacks PREAD and NOT PREAD bingo
table.add_rule(And(subject(X, Y), personal(Y), Not(legal_objection(Y))), PREAD(X, Y))
## rules= 14 safe= 59 unsafe= 0 time 7.291008
### R8 
# table.add_rule(medical(Y), data(Y))
# table.add_rule(diagnosis(Z), purpose(Z))
table.add_rule(doctor(Xr, X), And(anyone(X), anyone(Xr), Not(X==Xr))) # seem the right one
### more complex from anyone(Xr) and PREAD(Xr, Y) and legal_objection in the R4 case  
### => -2 thus not sufficient ... BUT look at 2+5+7+9 common in the 4 unsafe ??
### remove official => purpose is ok but what's the problem ?
### => anyone(X) & purpose(Z) from R1 et NOT => not official =/=legal ?
### => table.add_rule(legal(Z), official(Z)) semble ok
### rules= 15 safe= 83 unsafe= 0 time 10.272896
table.add_rule(And(subject(X, Y), medical(Y), doctor(Xr, X)), And(PREAD(Xr, Y), PWRITE(Xr, Y))) 
### rules= 16 safe= 108 unsafe= 0 time 12.7
### R9 !!! BTG break the glass not ussually permitted but allowed and monitored
### pour moi erreur BTG => normally denied

#### ======================
start = clock()
table.compute_table(table.number_rule())
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time " + str(clock()-start))
print (str(table))
#table.quine()
