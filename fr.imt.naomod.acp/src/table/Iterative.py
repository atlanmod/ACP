# ------------------
# 17/4/2018
# Iterative method
# remove obvious tautologies and separate unsafe  from safe
# -------------------

from Enumerative import  * #@UnusedWildImport
from Unsafe import *  #@UnusedWildImport
from Safe import *  #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
# Class for Iterative method inheriting Enumerative
# j will be the new rule and i one already seen
class Iterative(Enumerative):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        # local solver
        self.solver = Solver()
        # store safe cases
        self.safe = []
        # separate unsafe cases 
        self.unsafe = []
        # to store rules temporary 
        self.tempaux = []
        # to store information for last rule generation
        self.lastBinary = []
        self.lastNot = []
        # to count obvious
        self.obvious = 0
    # --- end init
    
    # --------------------
    def __str__(self):
        result = super().__str__()
        result += " ----------- Not unsafe -------------- \n"
        for er in self.safe:
            result += str(er) + "\n"
        result += " ----------- Unsafe -------------- \n"
        for e in self.unsafe:
            result += str(e) + "\n"
        return result 
    # --- end str
    
    # ---------------------
    def reset(self):
        super().reset()
        self.safe = []
        self.unsafe = []
        self.tempaux = []
        self.lastBinary = []
        self.lastNot = []
    # -- end reset
        
    # --------------------
    # Built the corresponding Z3 ExplRef from exclusive
    # without the ForAll quantifier
    def z3_safe(self):
        args = []
        rules = self.safe
        if (rules):
            for r in rules:
                args.append(r.z3())
            # -- end for
            return And(*args)
        else:
            return True
    # --- end of z3

    # --------------------
    # store only positive rules
    # Built the corresponding Z3 BoolRef from unsafe
    # without the  quantifiers
    def z3_unsafe(self):
        args = list(map(lambda x: x.z3(), self.unsafe))
        if (args):
            if (len(args)==1):
                return args[0]
            else:
                return And(*args)
        else:
            return True
    # --- end of z3_unsafe
    
    # --------------------
    # build the undefined expression with quantifiers
    def z3_undefined(self):
        args = []
        rules = self.unsafe
        # build exp for unsafe
        for r in rules:
            cond = r.get_cond()
            args.append(cond)
        # --- end for
        undef = self.one_undefined()
        if (is_expr(undef)):
            args.append(undef)
        else:
            args.extend(undef)
        if (args):
            return ForAll(self.variables, Or(*args))
        else:
            return False
    # --- end z3undefined
    
    # -------------------
    # Compute the union of 1-undefined in safe rules
    def one_undefined(self):
        args = []
        for r in self.safe:
            # optimize ?
            args.append(And(r.get_cond(), Not(r.get_conc())))
        if (args):
            return Or(*args)
        else:
            return False
    # --- end one-undefined

    #------------------
    # compute table with the new iterative process
    # take into account tautology and unsafe cases
    # with binary characteristic (in reverse counting order) and with don'tcare
    # bound is the number of processed rules (<= self.size()) and toview to print
    def compute_table(self, end):
        self.reset()
        self.clean(end)
        # j is the processed rule
        j = 1
        size = len(self.correct)
        # compute list of conditions and conclusions 
        # newrules only triple: binary, list conditions list conclusions
        rule = self.get_correct(0)
        # initialize with the first rule 
        if (rule.is_unsafe(self.variables)):
            self.unsafe = [Unsafe([1], [rule.get_cond()])]
        else:
            self.safe = [Safe([1], [rule.get_cond()], [rule.get_conc()])]
        self.lastNot = [Not(rule.get_cond())]
        self.lastBinary = [0]
        # iterative process for each sorted rule
        for j in range(1, size):
            rule = self.get_correct(j)
            #print ("----------  with rule " + str(j) + " = " + str(rule))
            new = rule.get_cond()
            negnew = Not(new)
            conc = rule.get_conc()
            self.computeNewRules(new, negnew, conc, j)
            j += 1
        # --- end for
    # -- end compute_table
    
    # ----------------------
    # compute the new rules and put in self.safe
    # nth number of the current correct and sorted rule
    def computeNewRules(self, new, negnew, conc, nth):
        self.tempaux = []
        nb_rules = len(self.safe)
        # check the empty case
        for k in range(0, nb_rules):
            # analyze existing rules
            rulek = self.safe[k] 
            binary = rulek.get_binary()
            lcond = Rule.get_cond(rulek)
            lconc = Rule.get_conc(rulek)
            # evaluate and store both new rules  
            newlcond = lcond + [new]  
            self.build(newlcond, lconc + [conc], binary+[1])
            # -- handle negative case
            newlcond =  lcond + [negnew] 
            self.build(newlcond, lconc, binary+[0])
        # -- end for k
        # add the last negative terms &_i ~D_i & ~D_j
        self.build(self.lastNot+[new], [conc], self.lastBinary+[1])
        # that is 2*existing rules + 1
        self.lastBinary.append(0)
        # update last negative conjunction 
        self.lastNot.append(negnew)
        # transfer to safe
        self.safe = []
        for r in self.tempaux:
            self.safe.append(Safe(r[0], r[1], r[2]))
    # --- end computeNewRules
 
    #------------------
    # compute table indicators
    # evaluate (list of) conds, concs 
    # return valid, unsafe (simple or general)
    def evaluate(self, conds, concs):
        #print ("evaluate " + str(conds) + " => " + str(concs))
        self.solver.reset()
        # check valid (unsat) only obvious 
        if ((len(conds) == 1) & isinstance(conds[0], bool)):
            self.solver.add(conds[0])
        else:
            self.solver.add(Exists(self.variables, And(*conds)))
        # --- end if conds
        valid = self.solver.check()
        self.solver.reset()
        if (valid.__eq__(unsat)):
            # count obvious
            self.obvious +=1
            return unsat, unsat
        else:
            # check general unsafe 
            self.solver.add(ForAll(self.variables, Or(Not(And(*conds)), And(*concs))))
            self.solver.add(Exists(self.variables, And(*conds)))
            unsafe = self.solver.check()
            self.solver.reset()
            return valid, unsafe
            # -- if unsafe
        # -- if valid
    # -- end evaluate
    
    # -------------------
    # build the rules, store unsafe and remove tautology
    # store new rule triple in tempaux
    # needs binary + last to store characteristic
    # remove all tautology, classify unsafe
    def build(self, conds, concs, binary):
        #print ("build for " + str(binary) + " : " + str(conds) + " " + str(concs) )
        valid, unsafe = self.evaluate(conds, concs)
        #print ("evaluate= " + str(valid) + " - " + str(unsafe))
        if (valid.__eq__(unknown) or unsafe.__eq__(unknown)):
            print ("Build unknown " + str(binary))
        if (valid.__eq__(sat)):
            if (unsafe.__eq__(unsat)):
                self.unsafe.append(Unsafe(binary, conds))
            else:
                self.tempaux.append((binary, conds, concs))
        # -- end if valid
    # -- end of build

    # --------------------------
    # check the validity of the transformation
    # self.rules <=> unsafe AND self.safe
    # take care of self.variables !!!  
    # TODO !!! do not take care of end should be with self.correct
    def check(self):
        # rules and Not(safe) OR Not(unsafe)
        self.solver.reset()
        self.solver.add(ForAll(self.variables, self.toBoolRef()))
        if (self.unsafe):
            self.solver.add(Exists(self.variables, Or(Not(self.z3_safe()), Not(self.z3_unsafe()))))
        else:
            self.solver.add(Exists(self.variables, Not(self.z3_safe())))
        #print (" => "  + str(self.solver))
        print (" => " + str(self.solver.check()))
        # Not(rules) AND safeAND unsafe
        self.solver.reset()
        self.solver.add(Exists(self.variables, Not(self.toBoolRef())))
        rprime = self.z3_safe()
        if (not isinstance(rprime, bool)):
            self.solver.add(ForAll(self.variables, rprime))
        if (self.unsafe):
            rprime = self.z3_unsafe()
            self.solver.add(ForAll(self.variables, rprime))
        #print ("<= " + str(self.solver))
        print (" <= " + str(self.solver.check()))
        self.solver.reset()
    # ----- end check
    
    # ----------------------
    # check safety of request set
    # check if REQ with quantifiers & undefined are disjoint
    def isSafe(self, REQ):
        self.solver.reset()
        self.solver.add(REQ)
        #print ("undefined ? " + str(self.z3undefined()))
        self.solver.add(self.z3_undefined())
        print ("isSafe " + str(REQ) + " is " + str(self.solver.check().__eq__(unsat)))
        self.solver.reset()
    # --- end isSafe
    
    # -------------------
    # compute union of conditions
    # this is the max defined expression
    def get_safe_conditions(self):
        res = list(map((lambda x: x.get_cond()), self.safe))
        if (res):
            if (len(res) == 1):
                return ForAll(self.variables, res[0])
            else:
                return ForAll(self.variables, Or(*res))
        else:
            return True
    # --- end get_safe_conditions
    
    # ----------------------
    # Check if REQ match at least one rule with a defined conclusion
    # REQ & +Not get_conditions unsat AND REQ & 1-undefined is sat
    # computation of safe(R) in IFM2018
    # TODO ???? optimise with binary ?
    def isDefined(self, REQ):
        self.solver.reset()
        self.solver.add(REQ)
        self.solver.push() # breakpoint
        self.solver.add(Not(self.get_safe_conditions()))
        match = self.solver.check()
        #print ("Solver: " + str(self.solver) + str(match))
        self.solver.pop()
        #print ("1-undefined= " + str(self.one_undefined()))
        self.solver.add(ForAll(self.variables, Not(self.one_undefined())))
        result = match.__eq__(unsat) and self.solver.check().__eq__(sat)
        #print ("Solver: " + str(self.solver) + str(self.solver.check()))
        self.solver.reset()
        print ("isDefined " + str(REQ) + " is " + str(result))
    # --- end isDefined
    
    # -------------------------
    # csv output of some tests
    # name is a local filename to create
    def perf(self, name):
        csvfile = open(name +".csv", "w+")
        try:
            outwriter = writer(csvfile)
            # use classe name here 
            outwriter.writerow( ['rules', 'correct', 'safe', 'unsafe', 'time'] )
            # for i in range(2, 31): #1+self.number_rule()):
            for i in range(2, 1+self.number_rule()):
                start = clock()
                self.compute_table(i)
                outwriter.writerow( [i,  len(self.correct), len(self.safe), len(self.unsafe), floor(clock()-start)])
                #print (str(self))
                print( str([i,  len(self.correct), len(self.safe), len(self.unsafe), floor(clock()-start)]))
        finally:
            csvfile.close()
    # ----- end of perf
    
 
# --- end class 