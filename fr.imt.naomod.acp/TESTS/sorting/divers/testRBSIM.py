# -------------------
# 26/4/2018
# example RBSSIM rule set #2 without uncertainty values 
# https://courses.csail.mit.edu/6.871/Assignment2/RBSSim.pdf
# -------------------

# TODO tester avec Iterative 
# 4 first avec relations au debut ou a la fin

from Sorting import * #@UnusedWildImport
#from Iterative import * #@UnusedWildImport
from time import * #@UnusedWildImport

# Sorts 
# TYPE = DeclareSort('TYPE')

table = Sorting()
#table = Iterative()
table.add_variable("CS", IntSort()) # Current Saving
table.add_variable("MS", IntSort()) # Monthly Salary
table.add_variable("NoY2R", IntSort()) # Number Of Years To Retirement
table.add_variable("AoOC", IntSort()) # Age of Oldest Child
table.add_variable("AGE", IntSort()) # Your Age
table.add_variable("AoYC", IntSort()) # Age Of Youngest Child 
# Variables ordered !
CS = table.get_variable(0)
MS = table.get_variable(1)
NoY2R = table.get_variable(2)
AoOC = table.get_variable(3)
AGE = table.get_variable(4)
AoYC = table.get_variable(5)

# predicates
#HHI = Function('HHI', TYPE, TYPE, BoolSort()) 

# ---------------- the constants 
# Have Health Insurance
HHI = Const('HHI', BoolSort())
# Basic Insurance Coverage = ADEQUATE or NOT
BIC = Const('BIC', BoolSort())
# Have Live Insurance
HLI = Const('HLI', BoolSort())
# Should Have Live Insurance
SHLI = Const('SHLI', BoolSort())
# 
Married = Const('Married', BoolSort())
Children = Const('Children', BoolSort())
# Category Of Fund = NONE
COFNone = Const('COFNone', BoolSort())
# Category Of Fund = MONEY MARKET 
COFMoney = Const('COFMoney', BoolSort())
# Category Of Fund = G&I = a mixed growth and income fund
COFGI = Const('COFGI', BoolSort())
# Category Of Fund = CONSERVATIVE GROWTH
COFCons = Const('COFCons', BoolSort())
# Category Of Fund = AGRESSIVE
COFAgressive = Const('COFAgressive', BoolSort())
# Category Of Fund = TAX-FREE
COFTaxFree = Const('COFTaxFree', BoolSort())
# Category Of Fund = INCOME
COFIncome = Const('COFIncome', BoolSort())
# Investment Goal = RETIREMENT 
IGRetired = Const('IGRetired', BoolSort())
# Investment Goal = CHILDREN'S EDUCATION 
IGChildren = Const('IGChildren', BoolSort())
# Investment Goal = HOME OWNERSHIP
IGHome = Const('IGHome', BoolSort())
# Investment Goal = CURRENT INCOME
IGIncome = Const('IGIncome', BoolSort())
# Investment Goal = INVEST SPARE CASH
IGCash = Const('IGCash', BoolSort())
# Risk Tolerance = LOW
RTLow = Const('RTLow', BoolSort())
# Risk Tolerance = MEDIUM
RTMedium = Const('RTMedium', BoolSort())
# Risk Tolerance = HIGH
RTHigh = Const('RTHigh', BoolSort())
# Tax Bracket = HIGH
Tax = Const('Tax', BoolSort())
# Life Stage = RETIRED or NOT
Retired = Const('Retired', BoolSort())
# Pension = NO or YES
Pension = Const('Pension', BoolSort())
# Individual Retirement Account = NO or YES
IRA = Const('IRA', BoolSort())
# Children Headed For College = YES or NO
CHC = Const('CHC', BoolSort())
# Children's Education Already Funded = YES or NO
CEAF = Const('CEAF', BoolSort())
# Own Home
Home = Const('Home', BoolSort())
# Want Home
Want = Const('Want', BoolSort())
# Enjoy Gambling = YES
Gambling = Const('Gambling', BoolSort())
# Budgeting Very Important = YES
Important = Const('Important', BoolSort())
# Worry About Money At Night = YES 
Worry = Const('Worry', BoolSort())
# Budget But Splurge Sometimes = YES
Budget = Const('Budget', BoolSort())
# College Tuition Level = CHEAP
College = Const('College', BoolSort())
# Children Have Scholarship = YES
Scholarship = Const('Scholarship', BoolSort())
# Children Eligible For Loans = YES
Loan = Const('Loan', BoolSort())
# Children Have Trust Fund = YES
Fund = Const('Fund', BoolSort())
# Children Headed For College = YES 
Headed = Const('Headed', BoolSort())

# ---------------- the rules 
# some implicit rules = 34
# # COF* are disjunct
# table.add_rule(And(COFNone, COFMoney), False) 
# table.add_rule(And(COFNone, COFGI), False) 
# table.add_rule(And(COFNone, COFCons), False) 
# table.add_rule(And(COFNone, COFAgressive), False) 
# table.add_rule(And(COFNone, COFTaxFree), False) 
# table.add_rule(And(COFNone, COFIncome), False) 
# # 
# table.add_rule(And(COFMoney, COFGI), False) 
# table.add_rule(And(COFMoney, COFCons), False) 
# table.add_rule(And(COFMoney, COFAgressive), False) 
# table.add_rule(And(COFMoney, COFTaxFree), False) 
# table.add_rule(And(COFMoney, COFIncome), False) 
# #
# table.add_rule(And(COFGI, COFCons), False) 
# table.add_rule(And(COFGI, COFAgressive), False) 
# table.add_rule(And(COFGI, COFTaxFree), False) 
# table.add_rule(And(COFGI, COFIncome), False) 
# #
# table.add_rule(And(COFCons, COFAgressive), False) 
# table.add_rule(And(COFCons, COFTaxFree), False)
# table.add_rule(And(COFCons, COFIncome), False)
# # 
# table.add_rule(And(COFAgressive, COFTaxFree), False) 
# table.add_rule(And(COFAgressive, COFIncome), False) 
# #
# table.add_rule(And(COFTaxFree, COFIncome), False) 
# IG* disjunct
# table.add_rule(And(IGRetired, IGChildren), False) 
# table.add_rule(And(IGRetired, IGCash), False) 
# table.add_rule(And(IGRetired, IGHome), False) 
# table.add_rule(And(IGRetired, IGIncome), False) 
# #
# table.add_rule(And(IGChildren, IGCash), False) 
# table.add_rule(And(IGChildren, IGHome), False) 
# table.add_rule(And(IGChildren, IGIncome), False)
# #
# table.add_rule(And(IGCash, IGHome), False) 
# table.add_rule(And(IGCash, IGIncome), False)  
# #
# table.add_rule(And(IGHome, IGIncome), False)  
# # RT* disjunct
# table.add_rule(And(RTLow, RTMedium), False) 
# table.add_rule(And(RTLow, RTHigh), False) 
# table.add_rule(And(RTMedium, RTHigh), False) 

### -----------------------------------
# ------------- business rules = 36
# # R2
table.add_rule(And(Not(HLI), SHLI), BIC)
# # R3
table.add_rule(And(HHI, HLI), BIC)
# ### here find an obvious conflict [Not(HHI), And(Not(HLI), SHLI)] 
# # # R4
table.add_rule(And(Married, Children), SHLI)
# R1 
table.add_rule(Not(HHI), Not(BIC))
# # R10
table.add_rule(Not(BIC), COFNone)
# # R11
table.add_rule(CS < 6*MS, COFMoney)
# # R12 
table.add_rule(And(IGRetired, NoY2R < 10), COFCons)
# # R13
table.add_rule(And(IGRetired, NoY2R > 10, NoY2R < 20), COFGI)
# # R14
table.add_rule(And(IGRetired, NoY2R > 20), COFAgressive)
# # R15
table.add_rule(And(IGChildren, AoOC < 7), COFGI)
# # R16
table.add_rule(And(IGChildren, AoOC > 7), COFCons)
# R17
table.add_rule(IGHome, COFGI)
# R18
table.add_rule(IGIncome, COFIncome)
# R19
table.add_rule(And(IGCash, RTLow), COFCons)
# R20
table.add_rule(And(IGCash, RTMedium), COFGI)
# R21
table.add_rule(And(IGCash, RTHigh), COFAgressive)
# R22
table.add_rule(And(IGCash, RTMedium, Tax), COFTaxFree)
# R23
table.add_rule(AGE < 67, Not(Retired))
# R24
table.add_rule(AGE >= 67, Retired)
# R31
table.add_rule(And(Not(Pension), IRA), IGRetired)
# R32
table.add_rule(And(Headed, Not(CEAF)), IGChildren)
# R33
table.add_rule(And(Not(Home), Want), IGHome)
# R34
table.add_rule(Retired, IGIncome)
# R35
table.add_rule(And(Home, Not(Want), Or(Pension, IRA), Or(Not(Children), CEAF), Not(Retired)), IGCash)
# R41
table.add_rule(Gambling, RTHigh)
# R42
table.add_rule(Important, RTLow)
# R43
table.add_rule(Worry, RTLow)
# R44
table.add_rule(Budget, RTMedium)
# R45
table.add_rule(And(Children, AoYC < 16), Headed)
# R46
table.add_rule(And(Children, AoYC >= 16), Not(Headed))
# R47
table.add_rule(Not(Children), Not(Headed))
# R51
table.add_rule(College, CEAF)
# R52
table.add_rule(Scholarship, CEAF)
# R53
table.add_rule(Loan, CEAF)
# R54
table.add_rule(Fund, CEAF)
# R55
table.add_rule(And(Not(Fund), Not(Loan), Not(Scholarship)), Not(CEAF))


start = clock()
#table.compute_table(20)  #  without exclu (deactivate check)  20 => safe= 10624 unsafe= 258 time= 677.862251
table.compute_table(30)  #  without exclu (deactivate check)  30 => NO one night
# table.compute_table(60)  #  with exclu  50 => 40s # 60 => 500s
# table.compute_table(54)  #  with exclu  54=34+20 => #rules= 70 safe= 182 unsafe= 458 time= 92.203131
# table.compute_table(70)  #  with exclu +check 70
#  => unsat
#  <= unsat
# #rules= 70 safe= 6234 unsafe= 11382 time= 4064.394305
#table.check() # 
#table.checkExclu()
#table.checkSingleExclu()
print ("#rules= " + str(table.number_rule()) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str((clock()-start))) 
#print (str(table))

