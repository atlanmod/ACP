# -------------------
# 22/4/2018
# Test Delmas2013
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

Person = DeclareSort('Person')
Information = DeclareSort('Information')
Topic = DeclareSort('Topic')

table = Sorting()
# Variables
table.add_variable("s", Person)
table.add_variable("r", Person)
table.add_variable("i", Information)
table.add_variable("t", Topic)
s = table.get_variable(0)
r = table.get_variable(1)
i = table.get_variable(2)
t = table.get_variable(3)

#  predicates 
Psend = Function('Psend', Person, Person, Information, BoolSort()) 
Fsend = Function('Fsend', Person, Person, Information, BoolSort()) 
Osend = Function('Osend', Person, Person, Information, BoolSort())
topic = Function('topic', Information, Topic, BoolSort())     
know = Function('know', Person, Information, BoolSort())

# Constants
tsunami = Const('tsunami', Topic)
military = Const('military', Topic)
TWC = Const('TWC', Person)

# exclusive 
table.add_rule(And(Psend(s, r, i), Fsend(s, r, i)), False)
#table.add_rule(And(topic(i, tsunami), know(s, i)), Osend(s, TWC, i))
table.add_rule(And(topic(i, military), know(s, i), Not(s==r)), Fsend(s, r, i))
table.add_rule(And(topic(i, tsunami), know(s, i), Not(s==r)), Psend(s, r, i))
### rather easy

table.compute_table(3)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))


