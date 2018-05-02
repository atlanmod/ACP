# -------------------
# 30/4/2018
# Test ArtOfProlog 
# -------------------
### program-2.1

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Type = DeclareSort('Type')

table = Sorting()
# Variables
table.add_variable("Uncle", Type)
table.add_variable("Person", Type)
table.add_variable("Parent", Type)
table.add_variable("Sib1", Type)
table.add_variable("Sib2", Type)
table.add_variable("Cousin1", Type)
table.add_variable("Cousin2", Type)
table.add_variable("Parent1", Type)
table.add_variable("Parent2", Type)
Uncle = table.get_variable(0)
Person = table.get_variable(1)
Parent = table.get_variable(2)
Sib1 = table.get_variable(3)
Sib2 = table.get_variable(4)
Cousin1 = table.get_variable(5)
Cousin2 = table.get_variable(6)
Parent1 = table.get_variable(7)
Parent2 = table.get_variable(8)

#  predicates 
uncle = Function('uncle', Type, Type, BoolSort()) 
brother = Function('brother', Type, Type, BoolSort()) 
parent = Function('parent', Type, Type, BoolSort()) 
sibling = Function('sibling', Type, Type, BoolSort()) 
cousin = Function('cousin', Type, Type, BoolSort()) 

#     uncle(Uncle,Person) :- brother(Uncle,Parent), parent(Parent,Person).
table.add_rule(And(brother(Uncle,Parent), parent(Parent,Person)), uncle(Uncle, Person))
#     sibling(Sib1,Sib2) :-  parent(Parent,Sib1), parent(Parent,SIb2), Sib1 \= Sib2.
table.add_rule(And(parent(Parent, Sib1), parent(Parent, Sib2), Not(Sib1 == Sib2)), sibling(Sib1, Sib2))
#    cousin(Cousin1,Cousin2) :-  parent(Parent1,Cousin1), parent(Parent2,Cousin2),   sibling(Parent1,Parent2).
table.add_rule(And(parent(Parent1,Cousin1), parent(Parent2,Cousin2), sibling(Parent1,Parent2)), cousin(Cousin1,Cousin2))
### rules= 3 safe= 7 unsafe= 0

#### =====================
start = clock()
table.compute_table(3)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str(floor(clock()-start)))
print (str(table))
### print(str(table.get_safe_conditions()))
#table.quine()
#table.perf("test")
