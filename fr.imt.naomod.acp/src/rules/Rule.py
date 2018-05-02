# ------------------
# 16/4/2018
# simple rule
# -------------------

from z3 import * #@UnusedWildImport
from z3.z3util import * #@UnusedWildImport

# --------------------
# conversion to TSPASS for a BoolRef
# requires self:BoolRef
def tspass(self):
    if (is_const(self)):
        return str(self) 
    elif (self == False):
        return "false"
    elif (self == True):
        return "true"    
    else:
        # it is an app
        return tspassApp(self)
# --- end tspass

# --------------------
# conversion to TSPASS for a BoolRef
# requires self:BoolRef it's an App ?
def tspassApp(self):
    op = self.decl().kind()
    sons = self.children()
    tmp = ""
    if (op == Z3_OP_AND):
        # could be 0,  1 and take care of the binary op
        size = len(sons)
        if (size > 0):
            tmp = Rule.PARIN + tspass(sons[0])
            for i in range(1, size):
                tmp += Rule.AND + tspass(sons[i])
            # --- for i
            tmp += Rule.PAROUT
        return tmp
    elif (op == Z3_OP_OR):
        # could be 0,  1 and take care of the binary op
        size = len(sons)
        if (size > 0):
            tmp = Rule.PARIN + tspass(sons[0])
            for i in range(1, size):
                tmp += Rule.OR + tspass(sons[i])
            # --- for i
            tmp += Rule.PAROUT
        return tmp
    elif (op == Z3_OP_NOT):
        return Rule.NOT +  Rule.PARIN + tspass(sons[0]) + Rule.PAROUT
    elif (op == Z3_OP_IMPLIES):
        return Rule.PARIN + tspass(sons[0]) + Rule.IMPLY + tspass(sons[1]) + Rule.PAROUT
    elif (op == Z3_OP_XOR):
        return "tspass:XOR not defined"
    elif (op == Z3_OP_EQ):
        # only for bool !!!
        return Rule.EQUAL + Rule.PARIN + tspass(sons[0]) + Rule.COMMA + tspass(sons[1]) + Rule.PAROUT
    elif (op == Z3_OP_DISTINCT):
        return Rule.NOT + Rule.EQUAL + Rule.PARIN + tspass(sons[0]) + Rule.COMMA + tspass(sons[1]) + Rule.PAROUT
    elif (op == Z3_OP_UNINTERPRETED):
        # case for predicates 
        return str(self)
    else:
        return "PB in tspass"
    # lacks specific predicates cases ?
    # --- end tspass  

# -----------------------------------------------------
# Class rule
# Free variables are assumed to be shared and declared at the top
# Implies(cond, conc) basically
class Rule():
    
    # TSPASS keywords 
    WHITE = ' '
    AND = ' & '
    OR = ' | ' # ????|||| pb italique ?
    NOT = ' ~'
    IMPLY = ' => '
    EQUIV = ' <=> '
    PARIN = '('
    PAROUT = ')'
    EQUAL = 'EQUAL '
    COMMA = ', '
    
    def __init__(self, cond, conc):
        # BoolRef condition
        self.cond = cond
        # BoolRef conclusion
        self.conc = conc
    # --- end init
    
    # --------------------
    def __str__(self):
        return "<" + str(self.cond) + " => " + str(self.conc) + ">"
    # --- end str
    
    # --------------------
    def tspass(self):
        return Rule.PARIN + tspass(self.get_cond()) + Rule.IMPLY + tspass(self.get_conc()) + Rule.PAROUT
    # --- end tspass
    
    # --------------------
    # generate a Z3 BoolRef
    def z3(self):
        cond = self.get_cond()
        conc = self.get_conc()
        return Implies(cond, conc)
    # --- end z3
    
    # --------------------
    # readers
    def get_cond(self):
        return self.cond
    def get_conc(self):
        return self.conc
    # --- end readers    
    
    # --------------------
    # setter
    def set_cond(self, new):
        self.cond = new
    def set_conc(self, new):
        self.conc = new
    # --- end setter
    
    # --------------------
    # test tautology and return yes or no
    # with free variables
    def is_tautology(self, variables):
        S = Solver()
        S.add(Exists(variables, And(self.get_cond(), Not(self.get_conc()))))
        return (S.check().__eq__(unsat))
    # --- end is_tautology     
    
    # --------------------
    # test unsafey and return yes or no
    # with free variables
    def is_unsafe(self, variables):
        S = Solver()
        S.add(ForAll(variables, self.z3()))
        cond = self.get_cond()
        if (isinstance(cond, bool)):
            S.add(cond)
        else:
            S.add(Exists(variables, cond))
        return (S.check().__eq__(unsat))
    # --- end is_unsafe   
    
# --- end Rule