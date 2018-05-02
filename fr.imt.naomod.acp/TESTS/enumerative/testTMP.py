# -------------------
# 16/4/2018
# tests TODO refaire les tests virer les commentaire
# -------------------
from z3.z3util import * #@UnusedWildImport
from Enumerative import * #@UnusedWildImport
from time import * #@UnusedWildImport

Type = DeclareSort('TYPE')
table = Enumerative()
# Variables
table.add_variable("X", Type)
table.add_variable("Y", Type)
#
X = table.get_variable(0)
Y = table.get_variable(1)

D0 = Function('D0', Type, BoolSort()) 
D1 = Function('D1', Type, BoolSort()) 
D2 = Function('D2', Type, BoolSort()) 
D3 = Function('D3', Type, BoolSort()) 
D4 = Function('D4', Type, BoolSort()) 
D5 = Function('D5', Type, BoolSort()) 
D6 = Function('D6', Type, BoolSort()) 
D7 = Function('D7', Type, BoolSort()) 
D8 = Function('D8', Type, BoolSort())
D9 = Function('D9', Type, BoolSort())  
C0 = Function('C0', Type, BoolSort()) 
C1 = Function('C1', Type, BoolSort()) 
C2 = Function('C2', Type, BoolSort()) 
C3 = Function('C3', Type, BoolSort()) 
C4 = Function('C4', Type, BoolSort()) 

INF = Function('<', Type, Type, BoolSort()) 
Q = Function('Q', Type, Type, BoolSort()) 
R = Function('R', Type, Type, BoolSort()) 

# ## chaining simple
# table.add_rule(D0(X), C0(X))
# table.add_rule(C0(X), C1(X))
# table.add_rule(C1(X), Not(D0(X)))
# ### we get 2 tautologies only ...

# # # example bizarre with last 
table.add_rule(INF(X, Y), Not(INF(Y, X)))
table.add_rule(INF(X, Y), Q(X, Y))
table.add_rule(Q(X, Y), R(Y, X))
table.add_rule(R(X, Y), Not(INF(X, Y))) 
# # seems corect attention inversion args

## unsafe seen after one step
# table.add_rule(D0(X), Not(D0(X)))
# table.add_rule(D1(X), C1(X))

# inclusion/exclusion ?
# table.add_rule(D0(X), And(C0(X), C1(X)))
# table.add_rule(D2(X), C2(X))
# table.add_rule(D1(X), C1(X))
# table.add_rule(D3(X), C0(X))

#### ==================================
### initial example arbitrary ordering 
# table.add_rule(D0(X), C0(X)) # 0
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D4(X), C1(X)) # 2
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(C3(X), D0(X)) # 4 
# table.add_rule(D3(X), And(C0(X), C1(X))) # 5 
# table.add_rule(D3(X), And(C2(X), C3(X))) # 6
# table.add_rule(D4(X), And(C0(X), C1(X))) # 7
# table.add_rule(D5(X), And(C2(X), C3(X))) # 8
# table.add_rule(D4(X), C4(X)) # 9
#### initial ordering 
# inclusions {0: [], 1: [], 2: [1], 3: [], 4: [], 5: [0, 1, 2], 6: [3], 7: [0, 1, 2, 5], 8: [3, 6], 9: []}
# exclusions {0: [], 1: [], 2: [1], 3: [], 4: [], 5: [], 6: [], 7: [5], 8: [6], 9: []}
# 10 safe= 19 unsafe= 20 time= 3.8768050000000005
### 31/3/2018
# 10 safe= 12 unsafe= 6 time= 2.634224
# {0: [], 1: [], 2: [], 3: [2], 4: [2, 3], 5: [], 6: [5], 7: [5, 6], 8: [2, 3], 9: [8, 2, 3]}

# reverse ordering 
# table.add_rule(D4(X), C4(X)) # 9
# table.add_rule(D5(X), And(C2(X), C3(X))) # 8
# table.add_rule(D4(X), And(C0(X), C1(X))) # 7
# table.add_rule(D3(X), And(C2(X), C3(X))) # 6
# table.add_rule(D3(X), And(C0(X), C1(X))) # 5 
# table.add_rule(C3(X), D0(X)) # 4 
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(D4(X), C1(X)) # 2
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D0(X), C0(X)) # 0
### reverse ordering
# inclusions {0: [], 1: [], 2: [], 3: [1], 4: [2], 5: [], 6: [], 7: [], 8: [7], 9: []}
# exclusions {0: [], 1: [], 2: [], 3: [1], 4: [2], 5: [], 6: [1, 3], 7: [2, 4], 8: [2, 4, 7], 9: [2, 4]}
# 10 safe= 13 unsafe= 9 time= 2.935369
### 31/3/2018
# 10 safe= 13 unsafe= 6 time= 2.610069
# {0: [], 1: [], 2: [], 3: [2], 4: [2, 3], 5: [], 6: [5], 7: [5, 6], 8: [5, 6], 9: [5, 6, 8]}
### why a diff avec les autres ?

# # ordering topo wrong
# table.add_rule(D0(X), C0(X)) # 0
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D4(X), C1(X)) # 2
# table.add_rule(D3(X), And(C0(X), C1(X))) # 5 
# table.add_rule(D4(X), And(C0(X), C1(X))) # 7
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(D3(X), And(C2(X), C3(X))) # 6
# table.add_rule(D5(X), And(C2(X), C3(X))) # 8
# table.add_rule(D4(X), C4(X)) # 9
# table.add_rule(C3(X), D0(X)) # 4 
### 4 9 without then last 
### 0 1 2 5 7 3 6 8 topo
# inclusions {0: [], 1: [], 2: [1], 3: [0, 1, 2], 4: [0, 1, 2, 3], 5: [], 6: [5], 7: [5, 6], 8: [], 9: []}
# exclusions {0: [], 1: [], 2: [1], 3: [], 4: [3], 5: [], 6: [], 7: [6], 8: [], 9: []}
# 10 safe= 19 unsafe= 28 time= 4.385611
#### 31/3/2018
# 10 safe= 12 unsafe= 6 time= 2.730706
# {0: [], 1: [], 2: [], 3: [2], 4: [2, 3], 5: [], 6: [5], 7: [5, 6], 8: [2, 3], 9: [8, 2, 3]}

# # reverse ordering topo
# table.add_rule(D3(X), And(C0(X), C1(X))) # 5 
# table.add_rule(D4(X), And(C0(X), C1(X))) # 7
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D4(X), C1(X)) # 2
# table.add_rule(D0(X), C0(X)) # 0
# table.add_rule(D3(X), And(C2(X), C3(X))) # 6
# table.add_rule(D5(X), And(C2(X), C3(X))) # 8
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(D4(X), C4(X)) # 9
# table.add_rule(C3(X), D0(X)) # 4 
# # inclusions {0: [], 1: [0], 2: [], 3: [2], 4: [], 5: [], 6: [5], 7: [], 8: [], 9: []}
# # exclusions {0: [], 1: [0], 2: [0, 1], 3: [0, 1, 2], 4: [0, 1], 5: [], 6: [5], 7: [5, 6], 8: [], 9: []}
# # 10 safe= 12 unsafe= 11 time= 3.111622
# ### semble meilleur 
### 31/3/2018
# 10 safe= 12 unsafe= 6 time= 2.739458
# {0: [], 1: [], 2: [], 3: [2], 4: [2, 3], 5: [], 6: [5], 7: [5, 6], 8: [2, 3], 9: [2, 3, 8]}


# # test with 3 6 8 all ordering
# table.add_rule(D5(X), And(C2(X), C3(X))) # 8
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(D3(X), And(C2(X), C3(X))) # 6
# ### 368=2+0+0.2  386=3+0+0.3  638=2+0+0.2 683=2+0+0.2 863=2+0+0.2 836=2+0+0.2

# # a different test less relation no conditions
# table.add_rule(D5(X), C4(X)) # 8bis
# table.add_rule(D4(X), And(C2(X), C3(X))) # 6bis
# table.add_rule(D3(X), C3(X)) # 3
# # 368=7+0+0.3  386=7+0+0.3  638=5+0+0.3 683=5+0+0.3 863= 5+0+0.3 836=7+0+0.3
# # 6 avant 3 ce qui est logique le 8 change peu

#### ------------
### another example arbitrary ordering but no conditions on relations
# table.add_rule(D0(X), C0(X)) # 0
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D2(X), C1(X)) # 2
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(D4(X), C2(X)) # 4 
# table.add_rule(D5(X), And(C0(X), C1(X))) # 5 
# table.add_rule(D6(X), And(C2(X), C3(X))) # 6
# table.add_rule(D7(X), And(C0(X), C1(X))) # 7
# table.add_rule(D8(X), And(C2(X), C3(X))) # 8
# table.add_rule(D9(X), C4(X)) # 9
### 
# inclusions {0: [], 1: [], 2: [1], 3: [], 4: [], 5: [0, 1, 2], 6: [3, 4], 7: [0, 1, 2, 5], 8: [3, 4, 6], 9: []}
# exclusions {0: [], 1: [], 2: [1], 3: [], 4: [], 5: [], 6: [], 7: [5], 8: [6], 9: []}
# 10 safe= 431 unsafe= 0 time= 16.913185000000002
### 31/3/2018
# 10 safe= 95 unsafe= 0 time= 6.9178809999999995
# {0: [], 1: [], 2: [1], 3: [1, 2], 4: [], 5: [4], 6: [4, 5], 7: [4, 5], 8: [1, 2], 9: [8, 1, 2]}

# ordering topo reverse 9 no rels 8 6 4 3 // 7 5 2 1 0 GOOD
# table.add_rule(D8(X), And(C2(X), C3(X))) # 8
# table.add_rule(D6(X), And(C2(X), C3(X))) # 6
# table.add_rule(D4(X), C2(X)) # 4 
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(D7(X), And(C0(X), C1(X))) # 7
# table.add_rule(D5(X), And(C0(X), C1(X))) # 5 
# table.add_rule(D2(X), C1(X)) # 2
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D0(X), C0(X)) # 0
# table.add_rule(D9(X), C4(X)) # 9
# inclusions {0: [], 1: [0], 2: [], 3: [], 4: [], 5: [4], 6: [], 7: [6], 8: [], 9: []}
# exclusions {0: [], 1: [0], 2: [0, 1], 3: [0, 1], 4: [], 5: [4], 6: [4, 5], 7: [4, 5, 6], 8: [4, 5], 9: []}
# 10 safe= 95 unsafe= 0 time= 5.185123
### 31/3/2018
# 10 safe= 95 unsafe= 0 time= 7.08732
# {0: [], 1: [], 2: [1], 3: [1, 2], 4: [1, 2], 5: [], 6: [5], 7: [5, 6], 8: [5, 6], 9: [5, 6, 8]}

## variante en permutant les rels
# table.add_rule(D9(X), C4(X)) # 9
# table.add_rule(D7(X), And(C0(X), C1(X))) # 7
# table.add_rule(D5(X), And(C0(X), C1(X))) # 5 
# table.add_rule(D2(X), C1(X)) # 2
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D0(X), C0(X)) # 0
# table.add_rule(D8(X), And(C2(X), C3(X))) # 8
# table.add_rule(D6(X), And(C2(X), C3(X))) # 6
# table.add_rule(D4(X), C2(X)) # 4 
# table.add_rule(D3(X), C3(X)) # 3
# inclusions {0: [], 1: [], 2: [1], 3: [], 4: [3], 5: [], 6: [], 7: [6], 8: [], 9: []}
# exclusions {0: [], 1: [], 2: [1], 3: [1, 2], 4: [1, 2, 3], 5: [1, 2], 6: [], 7: [6], 8: [6, 7], 9: [6, 7]}
# 10 safe= 95 unsafe= 0 time= 5.69682
#### 31/3/2018
# 10 safe= 95 unsafe= 0 time= 6.892561
# {0: [], 1: [], 2: [1], 3: [1, 2], 4: [], 5: [4], 6: [4, 5], 7: [4, 5], 8: [1, 2], 9: [1, 2, 8]}

### essai topo wrong ordering ?
# table.add_rule(D9(X), C4(X)) # 9
# table.add_rule(D0(X), C0(X)) # 0
# table.add_rule(D2(X), C1(X)) # 2
# table.add_rule(D1(X), C1(X)) # 1
# table.add_rule(D7(X), And(C0(X), C1(X))) # 7
# table.add_rule(D5(X), And(C0(X), C1(X))) # 5 
# table.add_rule(D3(X), C3(X)) # 3
# table.add_rule(D4(X), C2(X)) # 4 
# table.add_rule(D8(X), And(C2(X), C3(X))) # 8
# table.add_rule(D6(X), And(C2(X), C3(X))) # 6
# inclusions {0: [], 1: [], 2: [], 3: [2], 4: [1, 2, 3], 5: [1, 2, 3, 4], 6: [], 7: [], 8: [6, 7], 9: [6, 7, 8]}
# exclusions {0: [], 1: [], 2: [], 3: [2], 4: [], 5: [4], 6: [], 7: [], 8: [], 9: [8]}
# 10 safe= 431 unsafe= 0 time= 17.14361
### OK semble clair sur l'exemple
# ### 31/3/2018
# 10 safe= 95 unsafe= 0 time= 6.917062
# {0: [], 1: [], 2: [1], 3: [1, 2], 4: [], 5: [4], 6: [4, 5], 7: [4, 5], 8: [1, 2], 9: [8, 1, 2]}

# --------------
# #table.compute(False)
#table.clean()
#table.inclusions()
start = clock()
table.compute()
table.check()
table.checkExclu()
table.checkSingleExclu()
print (str(table.number_rule()) + " safe= " + str(len(table.exclusive)) +  " time= " + str((clock()-start))) 
# #table.quine()
print (str(table))
#print (str(table.dicoconcneg))

### ----------
#print(str(included([0], [1])))