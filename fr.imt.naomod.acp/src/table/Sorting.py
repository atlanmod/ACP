# ------------------
# 17/4/2018
# Table for exclusives rules
# obvious tautologies and all unsafe  +inclusions + sorting
# -------------------

from Iterative import *  #@UnusedWildImport
from Inclusion import * #@UnusedWildImport

# --------------------------
# Class for Table inheriting rule set 
# j will be the new rule and i one already seen
class Sorting(Iterative):
    
    # --------------------
    # init constructor 
    def __init__(self):
        super().__init__()
        # dicos for inclusion relations
        self.dicoconcneg = dict()  # ~Cj&Ci unsat
        # to store sorted rules
        self.sorted = []
    # --- end init
    
    # --------------------
    def __str__(self):
        result = ""
        #result = super().__str__()
#         result = RuleSet.__str__(self)
#         result += " ----------- Correct -------------- \n"
#         for r in self.correct:
#             result += str(r) + "\n"
        result += " ----------- Sorted -------------- \n"
        for r in self.sorted:
            result += str(r) + "\n"
        result += " ----------- Safe -------------- \n"
        for r in self.safe:
            result += str(r) + "\n"
        result += " ----------- Unsafe -------------- \n"
        for r in self.unsafe:
            result += str(r) + "\n"
        return result 
    # --- end str
    
    # ---------------------
    def reset(self):
        super().reset()
        self.sorted = []
        self.dicoconcneg = dict()
    # -- end reset
        
    
    # ----------------------
    def get_sorted(self, i):
        return self.sorted[i]
    # -- end get_sorted
 
    #------------------
    # Processing from the sorted rules ...
    # compute table with the new iterative process
    # take into account tautology and unsafe cases
    # with binary characteristic (in reverse counting order) and with don'tcare
    # bound is the number of processed rules (<= self.size()) and toview to print
    def compute_table(self, end):
        self.reset()
        self.clean(end)
        self.inclusions()
        # j is the processed rule
        j = 1
        size = len(self.sorted)
        # compute list of conditions and conclusions 
        # newrules only triple: binary, list conditions list conclusions
        rule = self.get_sorted(0)
        # initialize with the first rule 
        if (rule.is_unsafe(self.variables)):
            self.unsafe = [Unsafe([1], [rule.get_cond()])]
        else:
            self.safe = [Safe([1], [rule.get_cond()], [rule.get_conc()])]        
        self.lastNot = [Not(rule.get_cond())]
        self.lastBinary = [0]
        # iterative process for each sorted rule
        for j in range(1, size):
            rule = self.get_sorted(j)
            #print ("----------  with rule " + str(j) + " = " + str(rule))
            new = rule.get_cond()
            negnew = Not(new)
            conc = rule.get_conc()
            self.computeNewRules(new, negnew, conc, j)
            j += 1
        # --- end while
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
            # add here test exclusion
            rels = self.dicoconcneg[nth]
            # test if a rule in rels is active in binary
            if (included(rels, binary)):
                # copy the old rule with a dont'care
                # TODO optimize it no need of eval
                # self.build(lcond, lconc, binary+[-1])
                self.tempaux.append((binary+[-1], lcond, lconc))
            else:
                self.build(newlcond, lconc + [conc], binary+[1])
                # -- handle negative case
                newlcond =  lcond + [negnew] 
                self.build(newlcond, lconc, binary+[0])
            # --- end if 
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

    # -------------------------
    # Analyze (from correct rules) inclusions relations for conclusion only
    # with sorting the rules 
    # Need quantifiers 
    def inclusions(self):
        size = len(self.correct)
        # graph for topological sort 
        G = Inclusion(size)
        self.solver.reset()
        # analyze rule j
        for j in range(0, size):
            rulej = self.get_correct(j)
            Cj = rulej.get_conc()
            # compute relations with Cj => Ci and Ci => Cj
            for i in range(0, j):
                rulei = self.get_correct(i)
                Ci = rulei.get_conc()
                # check Cj&~Ci unsat
                #print ("inclusions " + str(Exists(self.variables, And(Cj, Not(Ci)))))
                self.solver.add(Exists(self.variables, And(Cj, Not(Ci))))
                sat = self.solver.check()
                self.solver.reset()
                if (sat.__eq__(unsat)):
                    #print("inclusions " + str(j) + " in " + str(i))
                    G.add(j, i)  
                # check ~Cj&Ci unsat
                #print ("inclusions " + str(Exists(self.variables, And(Not(Cj), Ci))))
                self.solver.add(Exists(self.variables, And(Not(Cj), Ci)))
                sat = self.solver.check()
                self.solver.reset()
                if (sat.__eq__(unsat)):
                    #print("inclusions " + str(i) + " in " + str(j))
                    G.add(i, j) 
            # -- end for i
        # -- end for j
        # sort the and sort the rules 
        #print ("graph " + str(G))
        G.sort()
        #print ("graph " + str(G))
        # TODO modif des sans relations possible ici on pourrait aussi separer les sans relations
        # reset sorted and inclusions relations
        self.sorted = [0]*size
        for i in range(0, size):
            self.dicoconcneg[i] = []
        for old in G.sorted:
            new = G.sorted[old]
            self.sorted[new] = self.get_correct(old)
            # transfer and sort relations before inc from neg to dicoconcneg
            # no inversion and forget greater relations
            if (old in G.dico):
                rels = G.dico[old]
                for inc in rels:
                    incnew = G.sorted[inc]
                    if (incnew > new):
                        self.dicoconcneg[incnew].append(new)
                # --- end for i
            # --- end if old
        #print("inclusions " + str(self.dicoconcneg))
    # --- end inclusions
    
# --- end class Sorting