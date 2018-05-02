# -------------------
# 2/5/2018
# CONTINUE A from test.tspass
# -------------------

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# Sorts
Subject = DeclareSort('Subject')
Resource = DeclareSort('Resource')

table = Sorting()
# Variables
table.add_variable("R", Resource)
table.add_variable("X", Subject)
R = table.get_variable(0)
X = table.get_variable(1)

# predicates
### subjects
subject = Function('subject', Subject, BoolSort()) 
admin = Function('admin', Subject, BoolSort()) 
pcchair = Function('pcchair', Subject, BoolSort()) 
pcmember= Function('pcmember', Subject, BoolSort()) 
subreviewer = Function('subreviewer', Subject, BoolSort()) 
### actions
Pdelete = Function('Pdelete', Subject, Resource, BoolSort()) 
Pcreate = Function('Pcreate', Subject, Resource, BoolSort()) 
Pread = Function('Pread', Subject, Resource, BoolSort()) 
Pwrite = Function('Pwrite', Subject, Resource, BoolSort()) 
Paction = Function('Paction', Subject, Resource, BoolSort()) 
### resources 
conference = Function('conference', Resource, BoolSort()) 
conferenceInfo = Function('conferenceInfo', Resource, BoolSort()) 
PcMember = Function('PcMember', Resource, BoolSort()) 
PcMemberAssignments = Function('PcMemberAssignments', Resource, BoolSort()) 
PcMemberConflicts = Function('PcMemberConflicts', Resource, BoolSort()) 
PcMemberInfo = Function('PcMemberInfo', Resource, BoolSort()) 
PcMemberInfoPassword = Function('PcMemberInfoPassword', Resource, BoolSort()) 

Paper = Function('Paper', Resource, BoolSort()) 
PaperSubmission = Function('PaperSubmission', Resource, BoolSort()) 
PaperDecision = Function('PaperDecision', Resource, BoolSort()) 
PaperConflicts = Function('PaperConflicts', Resource, BoolSort()) 
PaperAssignments = Function('PaperAssignments', Resource, BoolSort()) 
PaperReview = Function('PaperReview', Resource, BoolSort()) 
PaperReviewInfo = Function('PaperReviewInfo', Resource, BoolSort()) 
PaperReviewContent = Function('PaperReviewContent', Resource, BoolSort()) 
PaperReviewInfoSubmission = Function('PaperReviewInfoSubmission', Resource, BoolSort()) 

#### other predicates ?
PcMemberInfoischairflag = Function('PcMemberInfoischairflag', Resource, BoolSort()) 
isEQuserID = Function('isEQuserID', Subject, BoolSort()) 
isPending = Function('isPending', Subject, BoolSort()) 
isEQPaper = Function('isEQPaper', Subject, Resource, BoolSort()) 
MeetingFlag = Function('MeetingFlag', Resource, BoolSort()) 
isSubjectMeeting = Function('isSubjectMeeting', Subject, BoolSort()) 
isConflicted = Function('isConflicted', Subject, BoolSort()) 
isMeeting = Function('isMeeting', Subject, BoolSort()) 
isReviewInPlace = Function('isReviewInPlace', Subject, BoolSort()) 

# # #### these two seem sensible
# table.add_rule(pcchair(X), pcmember(X)) 
# table.add_rule(And(pcmember(X), subreviewer(X)), False) 
# # ------------------add disjunction rules
# # ### #admin and others ? subreviewer et pcmember/pchair
# # table.add_rule(And(admin(X), pcchair(X)), False) 
# # table.add_rule(And(admin(X), pcmember(X)), False) 
# # table.add_rule(And(admin(X), subreviewer(X)), False) 
# # table.add_rule(And(pcchair(X), subreviewer(X)), False)        
### exclusive actions just for showing a problem
# table.add_rule(And(Pdelete(X, R), Pcreate(X, R)), False)  # A1 - A6
# table.add_rule(And(Pdelete(X, R), Pread(X, R)), False)
# table.add_rule(And(Pdelete(X, R), Pwrite(X, R)), False)
# table.add_rule(And(Pcreate(X, R), Pread(X, R)), False)
# table.add_rule(And(Pcreate(X, R), Pwrite(X, R)), False)
# table.add_rule(And(Pread(X, R), Pwrite(X, R)), False)                       
# ### try with these disjunction about paper
# # Paper PaperSubmission PaperDecision PaperConflicts PaperAssignments PaperReview PaperReviewInfo PaperReviewContent PaperReviewInfoSubmission
# table.add_rule(And(Paper(R), PaperSubmission(R)), False) 
# table.add_rule(And(Paper(R), PaperDecision(R)), False) 
# table.add_rule(And(Paper(R), PaperConflicts(R)), False) 
# table.add_rule(And(Paper(R), PaperAssignments(R)), False) 
# table.add_rule(And(Paper(R), PaperReview(R)), False) 
# table.add_rule(And(Paper(R), PaperReviewInfo(R)), False) 
# table.add_rule(And(Paper(R), PaperReviewContent(R)), False) 
# table.add_rule(And(Paper(R), PaperReviewInfoSubmission(R)), False) 

# ---------------- the rules = 46+1
# (![x] ((admin(x) | pcchair(x) | pcmember (x) | subreviewer(x)) => subject(x)))
table.add_rule(Or(admin(X), pcchair(X), pcmember(X), subreviewer(X)), subject(X)) #1
# (![X, R] ((Pdelete(X, R) | Pcreate(X, R) | Pread(X, R) | Pwrite(X, R)) => Paction(X, R)))
table.add_rule(Paction(X, R), Or(Pdelete(X, R), Pcreate(X, R), Pread(X, R), Pwrite(X, R))) #2
# check with the reverse 
table.add_rule(Or(Pdelete(X, R), Pcreate(X, R), Pread(X, R), Pwrite(X, R)), Paction(X, R)) #2bis
# (![X, R] ((Conference(R) & admin(X)) => (Pread(X, R) & Pwrite(X, R))))
table.add_rule(And(conference(R), admin(X)), And(Pread(X, R), Pwrite(X, R))) #3
# # (![X, R] ((Conference(R) & pcchair(X)) => Pread(X, R)))
table.add_rule(And(conference(R), pcchair(X)), Pread(X, R)) #4
# # # (![X, R] ((Conference(R) & pcmember(X) & isMeeting(X)) => Pread(X, R)))
table.add_rule(And(conference(R), pcmember(X)), Pread(X, R)) #5
# # (![X, R] ((ConferenceInfo(R) & subject(X)) => Pread(X, R)))
table.add_rule(And(conferenceInfo(R), subject(X)), Pread(X, R)) #6
# # # (![X, R] ((PcMember(R) & pcmember(X)) => Pread(X, R))) 
table.add_rule(And(PcMember(R), pcmember(X)), Pread(X, R)) # 7  TODO verifier 
# # # (![X, R] ((PcMember(R) & admin(X)) => (Pcreate(X, R) & Pwrite(X, R))))
table.add_rule(And(PcMember(R), admin(X)), And(Pcreate(X, R), Pwrite(X, R))) #8
# # # (![X, R] ((PcMember(R) & pcmember(X) & isEQuserID(X)) => ~PAnyAction(X, R)))
table.add_rule(And(PcMember(R), pcmember(X), isEQuserID(X)), Not(Paction(X, R))) # +9 
# # # (![X, R] ((PcMember(R) & admin(X)) => Pdelete(X, R)))
table.add_rule(And(PcMember(R), admin(X)), Pdelete(X, R)) #10
# (![X, R] ((PcMemberAssignments(R) & pcchair(X)) => (Pread(X, R) & Pwrite(X, R))))
table.add_rule(And(PcMemberAssignments(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R))) # +11 
# (![X, R] ((PcMemberAssignments(R) & pcmember(X) & isEQuserID(X)) => Pread(X, R)))
table.add_rule(And(PcMemberAssignments(R), pcmember(X), isEQuserID(X)), Pread(X, R)) #12
# (![X, R] ((PcMemberConflicts(R) & pcchair(X)) => (Pread(X, R) & Pwrite(X, R))))
table.add_rule(And(PcMemberConflicts(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R))) #13
# (![X, R] ((PcMemberConflicts(R) & pcmember(X) & isEQuserID(X)) => Pread(X, R)))
table.add_rule(And(PcMemberConflicts(R), pcmember(X), isEQuserID(X)), Pread(X, R)) # 14
# (![X, R] ((PcMemberInfo(R) & pcchair(X)) => (Pread(X, R) & Pwrite(X, R))))
table.add_rule(And(PcMemberInfo(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R))) # 15
# (![X, R] ((PcMemberInfo(R) & pcmember(X) & isEQuserID(X)) => (Pwrite(X, R) & Pread(X, R))))
table.add_rule(And(PcMemberInfo(R), pcmember(X), isEQuserID(X)), And(Pread(X, R), Pwrite(X, R))) # 16
# (![X, R] ((PcMemberInfoPassword(R) & pcmember(X) & isEQuserID(X)) => Pwrite(X, R)))
table.add_rule(And(PcMemberInfoPassword(R), pcmember(X), isEQuserID(X)), Pwrite(X, R)) # 17
# (![X, R] ((PcMemberInfoPassword(R) & admin(X) & ~isPending(X)) => Pwrite(X, R)))
table.add_rule(And(PcMemberInfoPassword(R), admin(X), Not(isPending(X))), Pwrite(X, R))  # 18
# # (![X, R] ((PcMemberInfoischairflag(R) & pcmember(X)) => Pread(X, R)))
table.add_rule(And(PcMemberInfoischairflag(R), pcmember(X)), Pread(X, R)) # 19
# # (![X, R] ((PcMemberInfoischairflag(R) & pcmember(X) & isEQuserID(X)) => ~PAnyAction(X, R)))
table.add_rule(And(PcMemberInfoischairflag(R), pcmember(X), isEQuserID(X)), Not(Paction(X, R))) # 20
# (![X, R] ((PcMemberInfoischairflag(R) & admin(X)) => Pwrite(X, R))) 
table.add_rule(And(PcMemberInfoischairflag(R), admin(X)), Pwrite(X, R)) #21
# (![X, R] ((Paper(R) & pcchair(X)) => Pdelete(X, R)))
table.add_rule(And(Paper(R), pcchair(X)), Pdelete(X, R)) #22
# (![X, R] ((Paper(R) & pcmember(X) & isEQPaper(X, R)) => Pread(X, R)))
table.add_rule(And(Paper(R), pcmember(X), isEQPaper(X, R)), Pread(X, R)) #23
# (![X, R] ((Paper(R) & pcmember(X)) => Pcreate(X, R)))
table.add_rule(And(Paper(R), pcmember(X)), Pcreate(X, R)) #24
# (![X, R] ((PaperSubmission(R) & (pcmember(X) | pcchair(X))) => Pread(X, R))) 
table.add_rule(And(PaperSubmission(R), Or(pcmember(X), pcchair(X))), Pread(X, R)) #25
# (![X, R] ((PaperSubmission(R) & subreviewer(X) & isEQuserID(X)) => Pread(X, R)))
table.add_rule(And(PaperSubmission(R), subreviewer(X), isEQuserID(X)), Pread(X, R)) #26
# (![X, R] ((PaperDecision(R) & pcchair(X) & isSubjectMeeting(X)) => (Pread(X, R) & Pwrite(X, R))))
table.add_rule(And(PaperDecision(R), pcchair(X), isSubjectMeeting(X)), And(Pread(X, R), Pwrite(X, R))) #27
# (![X, R] ((PaperConflicts(R) & (admin(X) | pcchair(X))) => (Pwrite(X, R) & Pread(X, R))))
table.add_rule(And(PaperConflicts(R), Or(admin(X), pcchair(X))), And(Pread(X, R), Pwrite(X, R))) #28
# (![X, R] ((PaperConflicts(R) &  pcmember(X) & isConflicted(X)) =>  Pread(X, R)))
table.add_rule(And(PaperConflicts(R), pcmember(X), isConflicted(X)), Pread(X, R)) #29
# (![X, R] ((PaperConflicts(R) &  pcmember(X) & isMeeting(X)) =>  Pread(X, R)))
table.add_rule(And(PaperConflicts(R), pcmember(X), isMeeting(X)), Pread(X, R)) #30
# (![X, R] ((PaperConflicts(R) & subject(X) & isConflicted(X)) => ~Paction(X, R)))
table.add_rule(And(PaperConflicts(R), subject(X), isConflicted(X)), Not(Paction(X, R)))
# (![X, R] ((PaperAssignments(R) & (admin(X) | pcchair(X))) => (Pwrite(X, R) & Pread(X, R))))
table.add_rule(And(PaperAssignments(R), Or(admin(X), pcchair(X))), And(Pread(X, R), Pwrite(X, R)))
# (![X, R] ((PaperAssignments(R) & subject(X) & isConflicted(X)) => (~Pcreate(X, R) & ~Pwrite(X, R) & ~Pread(X, R))))
table.add_rule(And(PaperAssignments(R), subject(X), isConflicted(X)), And(Not(Pread(X, R)), Not(Pwrite(X, R)), Not(Pcreate(X, R))))
# (![X, R] ((PaperAssignments(R) & isEQPaper(X, R) & pcchair(X) & isSubjectMeeting(X)) => Pread(X, R)))
table.add_rule(And(PaperAssignments(R), isEQPaper(X, R), pcchair(X), isSubjectMeeting(X)), Pread(X, R))
# (![X, R] ((PaperAssignments(R) & subject(X) & isSubjectMeeting(X)) =>  ~Pread(X, R)))
table.add_rule(And(PaperAssignments(R), subject(X), isSubjectMeeting(X)), Not(Pread(X, R)))
# (![X, R] ((PaperReview(R) & pcchair(X) & ~isConflicted(X)) => Paction(X, R)))
table.add_rule(And(PaperReview(R), pcchair(X), Not(isConflicted(X))), Paction(X, R))
# (![X, R] ((PaperReview(R) & isEQPaper(X, R) & pcchair(X) & isSubjectMeeting(X)) => Pread(X, R)))
table.add_rule(And(PaperReview(R), isEQPaper(X, R), pcchair(X), isSubjectMeeting(X)), Pread(X, R))
# (![X, R] ((PaperReview(R) & pcchair(X)) => (Pdelete(X, R) & Pcreate(X, R))))
table.add_rule(And(PaperReview(R), pcchair(X)), And(Pdelete(X, R), Pcreate(X, R)))
# (![X, R] ((PaperReview(R) & subject(X) & isConflicted(X)) => ~Paction(X, R)))
table.add_rule(And(PaperReview(R), subject(X), isConflicted(X)), Not(Paction(X, R)))
# (![X, R] ((PaperReview(R) &  pcmember(X) & ~isConflicted(X)) =>  Pread(X, R)))
table.add_rule(And(PaperReview(R), pcmember(X), Not(isConflicted(X))), Pread(X, R))
# (![X, R] ((PaperReviewInfo(R) & pcchair(X)) => Paction(X, R)))
table.add_rule(And(PaperReviewInfo(R), pcchair(X)), Paction(X, R))
# (![X, R] ((PaperReviewContent(R) & pcmember(X) & isEQuserID(X)) => (Pcreate(X, R) & Pwrite(X, R) & Pdelete(X, R))))
table.add_rule(And(PaperReviewContent(R), pcmember(X), isEQuserID(X)), And(Pcreate(X, R), Pwrite(X, R), Pdelete(X, R)))
# (![X, R] ((PaperReviewContent(R) & subreviewer(X) & isEQuserID(X)) => Pcreate(X, R)))
table.add_rule(And(PaperReviewContent(R), subreviewer(X), isEQuserID(X)), Pcreate(X, R))
# (![X, R] ((PaperReviewInfoSubmission(R) & pcmember(X) & isEQuserID(X) & isReviewInPlace(X)) => Pwrite(X, R) ))
table.add_rule(And(PaperReviewInfoSubmission(R), pcmember(X), isEQuserID(X), isReviewInPlace(X)), Pwrite(X, R))
# (![X, R] ((MeetingFlag(R) & pcchair(X)) => (Pread(X, R) & Pwrite(X, R))))
table.add_rule(And(MeetingFlag(R), pcchair(X)), And(Pread(X, R), Pwrite(X, R)))
# (![X, R] ((MeetingFlag(R) & pcmember(X)) => Pread(X, R)))
table.add_rule(And(MeetingFlag(R), pcmember(X)), Pread(X, R))

# table.computeTable2(46, True)
# table.check() # TODO refaire 1a1 avec les autres tests
# # print (str(table.size()) + " safe= " + str(len(table.exclusive)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str((clock()-start))) 

start = clock()
table.compute_table(47)
#table.compute_table(48)
#table.compute_table(57)
table.check() # 
#table.checkExclu()
#table.checkSingleExclu()
print (str(len(table.rules)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str((clock()-start))) 
print ("obvious= " + str(table.obvious))
# print (str(table))
# ##### ======== sans les disjunct 47
# inclusions {0: [], 1: [], 2: [], 3: [1], 4: [2], 5: [2], 6: [2, 5], 7: [2, 5, 6], 8: [2, 4, 5], 9: [2, 4, 5, 8], 10: [], 11: [10], 12: [10, 11], 13: [], 14: [13], 15: [13, 14], 16: [13, 14, 15], 17: [], 18: [17], 19: [17, 18], 20: [17, 18, 19], 21: [17, 18, 19, 20], 22: [17, 18, 19, 20, 21], 23: [17, 18, 19, 20, 21, 22], 24: [17, 18, 19, 20, 21, 22, 23], 25: [17, 18, 19, 20, 21, 22, 23, 24], 26: [2, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25], 27: [2, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26], 28: [2, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], 29: [2, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], 30: [17, 18, 19, 20, 21, 22, 23, 24, 25], 31: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30], 32: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31], 33: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32], 34: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33], 35: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34], 36: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35], 37: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36], 38: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37], 39: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38], 40: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], 41: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], 42: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], 43: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], 44: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43], 45: [17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44], 46: [2, 4, 5, 6, 7, 8, 9, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]}
#  => unsat
#  <= unsat
# safe= 302 unsafe= 530 time= 174.378204
# 47 safe= 302 unsafe= 530 time= 165.540094
# 24/4/2018 perf %3 with optimization on inclusion
# #obvious= obvious= 938
### testA.txt contient la table
### first PB avec rules: 
# <Or(admin(X), pcchair(X), pcmember(X), subreviewer(X)) => subject(X)>
# <And(PaperAssignments(R), subject(X), isConflicted(X)) => And(Not(Pread(X, R)), Not(Pwrite(X, R)), Not(Pcreate(X, R)))>
# <And(PaperReviewContent(R), pcmember(X), isEQuserID(X)) => And(Pcreate(X, R), Pwrite(X, R), Pdelete(X, R))>
### tres bien 

#### ================== avec les 46 sans la 2bis
#  => unsat
#  <= unsat
# 46 safe= 922 unsafe= 488 time= 423.28515000000004
### 46 safe= 922 unsafe= 488 time= 408.029412

#### cas avec les dijucnt sur actions qui ne sont pas correctes
#### ============= avec les 11 disjunct
#### safe= 43 unsafe= 470 time= 80.54808999999999
#### ============== avec les 11 sans le check
#### safe= 43 unsafe= 470 time= 70.604839
#### ================ 47+8+2 
### 47+2sensibles +8 Paper* 57 safe= 241 unsafe= 535 time= 100.196482
### 57 safe= 241 unsafe= 535 time= 96.692969
### result in testA57.txt

# #### check inclusion in the safe conditions or not 
# S = Solver()
# S.add(Not(table.get_safe_conditions()))
# S.push()
# #S.add(ForAll([X, R], And(PaperReviewContent(R), pcmember(X), isEQuserID(X)))) ### sat
# #S.add(ForAll([X, R], And(Not(PcMember(R)), PaperReviewContent(R), pcmember(X), isEQuserID(X)))) ### sat
# # S.add(ForAll([X, R], And(Not(PcMember(R)), PaperReviewContent(R), pcmember(X), Not(subreviewer(X)), isEQuserID(X)))) ### sat
# S.add(ForAll([X, R], And(Not(subreviewer(X)), Not(Paper(R)), pcchair(X), admin(X), Not(PaperAssignments(R)), PaperReviewContent(R), 
#      pcmember(X), isEQuserID(X), Pdelete(X, R), Not(PcMember(R)), Not(PcMemberInfoischairflag(R)), Not(PaperConflicts(R)), 
#      Not(PaperReview(R)), conference(R)))) ### oui unsat 
# print (" cas 1  " + str(S.check()))
# # S.pop()
# # S.add(ForAll([X, R], And(Not(pcchair(X)), PaperReviewContent(R), pcmember(X), isEQuserID(X)))) ### sat
# # print (" cas 2  " + str(S.check()))
# print (" time after check = " + str((clock()-start))) 

# # simplif first safe condition ?
# print(str(tactic(And(Not(And(pcmember(X), subreviewer(X))), Not(And(Paper(R), PaperSubmission(R))), Not(And(Paper(R), PaperDecision(R))),
#             Not(And(Paper(R), PaperConflicts(R))), Not(And(Paper(R), PaperAssignments(R))), Not(And(Paper(R), PaperReview(R))),
#             Not(And(Paper(R), PaperReviewInfo(R))), Not(And(Paper(R), PaperReviewContent(R))), 
#             Not(And(Paper(R), PaperReviewInfoSubmission(R))), pcchair(X), Or(admin(X), pcchair(X), pcmember(X), subreviewer(X)),
#             Not(And(PaperAssignments(R), subject(X), isConflicted(X))), And(PaperReviewContent(R), pcmember(X), isEQuserID(X)),
#             Not(And(PaperAssignments(R), subject(X), isSubjectMeeting(X))), 
#             Or(Pdelete(X, R), Pcreate(X, R), Pread(X, R), Pwrite(X, R)), Not(And(PcMember(R), pcmember(X), isEQuserID(X))), 
#             Not(And(PcMemberInfoischairflag(R), pcmember(X), isEQuserID(X))), 
#             Not(And(PaperConflicts(R), subject(X), isConflicted(X))), Not(And(PaperReview(R), subject(X), isConflicted(X))),
#             And(conference(R), admin(X))))))
# ### rame un des morceaux 
# And(Not(subreviewer(X)), Not(Paper(R)), pcchair(X), admin(X), Not(PaperAssignments(R)), PaperReviewContent(R), 
#     pcmember(X), isEQuserID(X), Pdelete(X, R), Not(PcMember(R)), Not(PcMemberInfoischairflag(R)), Not(PaperConflicts(R)), 
#     Not(PaperReview(R)), conference(R))

######## 47+A1-A6
#  => unsat
#  <= unsat
# 53 safe= 43 unsafe= 517 time= 70.160953
#### et avec seulement +A6
###48 safe= 101 unsafe= 732 time= 86.628282

#### ==================
# CSV output
# table.perf("sorting47")
# table.perf("sortingMore") +2rule du debut bof
### essai +8 papers
#table.perf("sorting47+8") 
#table.perf("sorting47+A1-6") 
# table.perf("sorting47+8+2") 



