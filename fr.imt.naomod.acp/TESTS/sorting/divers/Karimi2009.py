# -------------------
# 22/4/2018
# Test Karimi2009
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

Resource = DeclareSort('Resource')
Agent = DeclareSort('Agent')

table = Sorting()
# Variables
table.add_variable("cre", Agent)
table.add_variable("cu", Agent)
table.add_variable("m", Resource)
table.add_variable("c", Resource)
cre = table.get_variable(0)
cu = table.get_variable(1)
m = table.get_variable(2)
c = table.get_variable(3)

#  predicates 
resource = Function('resource', Resource, BoolSort()) 
agent = Function('agent', Agent, BoolSort()) 
money = Function('money', Resource, BoolSort()) 
car = Function('car', Resource, BoolSort()) 
employee = Function('employee', Agent, BoolSort()) 
customer = Function('customer', Agent, BoolSort()) 
gold = Function('gold', Agent, BoolSort()) 
rent = Function('rent', Agent, Agent, Resource, BoolSort()) 
price = Function('price', Resource, Resource, BoolSort()) 
receipt = Function('rent', Agent, Agent, Resource, BoolSort()) 
discount = Function('discount', Agent, Resource, BoolSort()) 

# (![m] (Money(m) => Resource(m))) &
# (![c] (Car(c) => Resource(c))) &
# (![m] ~(Money(m) & Car(m))) & %%% disjoint
# (![cre] (CarRentalEmployee(cre) => Agent(cre))) &
# (![cu] (Customer(cu) => Agent(cu))) &
# (![g] (GoldClub(g) => Customer(g))) &
# (![cre,cu,m,c] ((CarRentalEmployee(cre) & Customer(cu) & ~same(cre, cu) & Money(m) & Car(c) & rentACar(cre, cu, c) & price(c, m)) => cashReceipt(cu, cre, m))) &
# %%% P1: golden case discount : soit le reçoive soit il est déduit ...
# (![cre,cu,m,c] ((CarRentalEmployee(cre) & GoldClub(cu) & ~same(cre, cu) & Money(m) & Car(c) & rentACar(cre, cu, c) & price(c, m)) => (cashReceipt(cu, cre, m) & discount(cre, m))))

table.add_rule(money(m), resource(m))
table.add_rule(car(c), resource(c))
table.add_rule(And(money(m), car(m)), False)
table.add_rule(employee(cre), agent(cre))
table.add_rule(customer(cu), agent(cu))
table.add_rule(gold(cu), customer(cu))
table.add_rule(And(employee(cre), customer(cu), Not(cre==cu), money(m), car(c), rent(cre, cu, c), price(c, m)), 
               receipt(cu, cre, m))
table.add_rule(And(employee(cre), gold(cu), Not(cre==cu), money(m), car(c), rent(cre, cu, c), price(c, m)),
               And(receipt(cu, cre, m), discount(cre, m)))
### wihtout that only "trivial" from 1 existing rule ?
#  ((CarRentalEmployee(x) & Customer(x) & rentACar(x, x, c) & price(c,m)) => not discount
table.add_rule(And(employee(cre), customer(cre), car(c), rent(cre, cre, c), price(c, m)), Not(discount(cre, m)))
# the last new unsafe ? more obvious with only the three critical rules ...

table.compute_table(9)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)))
print (str(table))
table.quine() # good example with 6 first or 9

