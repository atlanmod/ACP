# ------------------
# 20/4/2018
# Table for exclusive rules and enumerative
# -------------------

from ExclusiveRule import * #@UnusedWildImport
from RuleSet import * #@UnusedWildImport
from MoreUtility import * #@UnusedWildImport
from csv import * #@UnusedWildImport
from time import * #@UnusedWildImport
from math import * #@UnusedWildImport

# --------------------------
# Class for Table inheriting rule set 
class Enumerative(RuleSet):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        # to store exclusive rules a list of rules
        # binary characteristic = dec2bin(index+1)
        self.exclusive = []
        # local solvers
        self.solver = Solver()
        # to store non tautology
        self.correct = []
    # --- end init
    
    # --------------------
    def __str__(self):
        result = super().__str__()
        result += "\n ----------- Correct -------------- \n"
        for r in self.correct:
            result += str(r) + "\n"
        result += " ----------- Exclusive -------------- \n"
        for er in self.exclusive:
            result += str(er) + "\n"
        return result 
    # --- end str
    
    # ---------------------
    def reset(self):
        self.exclusive = []
        self.correct = []
    # -- end reset
        
    # ----------------------
    def get_correct(self, i):
        return self.correct[i]
    # -- end get_correct

    # -------------------
    # compute list of conditions
    def get_conds(self):
        return list(map((lambda x: x.get_cond()), self.correct))
    # --- end get_conds
    
    # -------------------
    # compute list of conclusions
    def get_concs(self):
        return list(map((lambda x: x.get_conc()), self.correct))
    # --- end get_concs

    # ------------------------
    # check each rule, clean obvious rules
    # and remove only tautologies 
    # end last rule to stop analysis
    def clean(self, end):
        self.correct = []
        for i in range(0, end):
            r = self.rules[i]
            if (not r.is_tautology(self.variables)):
                self.correct.append(r)
        # -- end for
    # -- end clean

    # --------------------
    # Enumerative computation
    # without simplification but respecting the binary characteristic
    # same quantifiers as the original rules
    # end to only process the first end rules
    def compute_table(self, end):
        # remove tautology
        self.clean(end)
        # size of the rule set 
        n = len(self.correct)
        # compute list of conditions and conclusions 
        conds = self.get_conds()
        concs = self.get_concs()
        # print ("liste " + str(conds) + " " + str(concs))
        limit = 2 ** n
        # enumerate non void combinaitions of [1 .. n]
        # it is a list of binary digits of length n 
        for j in range(1, limit):
            # compute the binary characteristic
            charac = dec2bin(j, n)
            complexcond = []
            complexconc = []
            for i in range(0, n):
                if (charac[i]==1):
                    complexcond = complexcond + [conds[i]]
                    complexconc = complexconc + [concs[i]]
                else:
                    complexcond = complexcond + [Not(conds[i])] 
                # -- end if
            # -- end for i
            # n is surely >=2 thus an and is needed
            complexcond = And(*complexcond)
            if (len(complexconc) > 1):
                complexconc = And(*complexconc)
            else:
                complexconc = complexconc[0]
            # -- end if
            #  test and remove tautology
            # reset solvers 
            self.solver.reset()
            self.solver.add(Exists(self.variables, And(complexcond, Not(complexconc))))
            valid = self.solver.check()
            if (not valid.__eq__(unsat)):
                self.exclusive.append(ExclusiveRule(charac, complexcond, complexconc))
        # -- end for j
    # --- end compute_table

    # --------------------
    # Built the corresponding Z3 ExpRef
    # without the ForAll quantifier
    def z3_exclusive(self):
        args = []
        rules = self.exclusive
        if (rules):
            for r in rules:
                args.append(r.z3())
            # -- end for
            return And(*args)
        else:
            return True
    # --- end of z3

    # --------------------------
    # check the validity of the transformation
    # self.rules <=> self.exclusive
    def check(self):
        # rules and Not(exclusive) 
        self.solver.reset()
        self.solver.add(ForAll(self.variables, self.toBoolRef()))
        self.solver.add(Exists(self.variables, Not(self.z3_exclusive())))
        #print (" => "  + str(self.solver))
        print (" => " + str(self.solver.check()))
        self.solver.reset()
        self.solver.add(Exists(self.variables, Not(self.toBoolRef())))
        rprime = self.z3_exclusive()
        if (not isinstance(rprime, bool)):
            self.solver.add(ForAll(self.variables, rprime))
        #print ("<= " + str(self.solver))
        print (" <= " + str(self.solver.check()))
    # ----- end check
    
    # ----------------------
    # check pair wise exclusivity of conditions
    def checkExclu(self):
        print ("check condition exclusivity ...... ")
        for j in range(0, len(self.exclusive)):
            condj = self.exclusive[j].get_cond()
            for i in range(j+1, len(self.exclusive)):
                condi = self.exclusive[i].get_cond()
                self.solver.reset()
                self.solver.add(ForAll(self.variables, And(condj, condi)))
                if (not self.solver.check().__eq__(unsat)):
                    print ("checkExclu problem with " + str(j) + " " + str(i))
                    print ("rules j & i " + str(self.exclusive[j]) + " \n " + str(self.exclusive[i]))
            # -- end for i
        # --- end for j
    # --- end checkExclu
    
    # ----------------------
    # check pair wise exclusivity on binary
    def checkSingleExclu(self):
        print ("check binary exclusivity ...... ")
        for j in range(0, len(self.exclusive)):
            binj = self.exclusive[j].get_binary()
            for i in range(j+1, len(self.exclusive)):
                bini = self.exclusive[i].get_binary()
                if (binj == bini):
                    print ("checkSingleExclu problem with " + str(j) + " " + str(i))
            # -- end for i
        # --- end for j
    # --- end checkSingleExclu
    
    # -------------------------
    # csv output of some tests
    # name is a local filename to create
    def perf(self, name):
        csvfile = open(name +"20.csv", "w+")
        try:
            start = clock()
            outwriter = writer(csvfile)
            outwriter.writerow( ['Enumerative'] )
            outwriter.writerow( ['rule', 'correct', 'exclusive', 'time'] )
            for i in range(2, 21): #self.number_rule()):
                self.compute_table(i)
                outwriter.writerow( [i , len(self.correct),  len(self.exclusive) ,  floor((clock()-start))])
                print( str([i , len(self.correct),  len(self.exclusive) ,  floor((clock()-start))]))
        finally:
            csvfile.close()
    # ----- end of perf

    # ----------------------------
    # rebuild a  condition list of BoolRef from a binary characteristic
    # and return the list of conditions
    def rebuildCond(self, binary):
        res = []
        for i in range(0, len(binary)):
            if (not binary[i] == -1):
                if (binary[i] == 1):
                    res.append(self.get_sorted(i).get_cond())
                else:
                    res.append(Not(self.get_sorted(i).get_cond()))
                # -- useful case
            # -- don't care
        # -- for i
        return res
    # --- end rebuildCond
    
# --- end Enumerative