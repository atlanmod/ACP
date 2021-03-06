# -------------------
# 20/6/2018
# CONTINUE A from test.tspass
# -------------------

from Enumerative import * #@UnusedWildImport
from time import * #@UnusedWildImport

# Sorts
Subject = DeclareSort('Subject')
Resource = DeclareSort('Resource')

table = Enumerative()
# Variables
table.add_variable("R", Resource)
table.add_variable("X", Subject)
R = table.get_variable(0)
X = table.get_variable(1)

# predicates
subject = Function('subject', Subject, BoolSort()) 
admin = Function('admin', Subject, BoolSort()) 
pcchair = Function('pcchair', Subject, BoolSort()) 
pcmember= Function('pcmember', Subject, BoolSort()) 
subreviewer = Function('subreviewer', Subject, BoolSort()) 
Pdelete = Function('Pdelete', Subject, Resource, BoolSort()) 
Pcreate = Function('Pcreate', Subject, Resource, BoolSort()) 
Pread = Function('Pread', Subject, Resource, BoolSort()) 
Pwrite = Function('Pwrite', Subject, Resource, BoolSort()) 
Paction = Function('Paction', Subject, Resource, BoolSort()) 
conference = Function('conference', Resource, BoolSort()) 
conferenceInfo = Function('conferenceInfo', Resource, BoolSort()) 
PCmember = Function('PCmember', Resource, BoolSort()) 
isEQuserID = Function('isEQuserID', Subject, BoolSort()) 
PcMemberAssignments = Function('PcMemberAssignments', Resource, BoolSort()) 
PcMemberConflicts = Function('PcMemberConflicts', Resource, BoolSort()) 
PcMemberInfo = Function('PcMemberInfo', Resource, BoolSort()) 
PcMemberInfoPassword = Function('PcMemberInfoPassword', Resource, BoolSort()) 
PcMemberInfoischairflag = Function('PcMemberInfoischairflag', Resource, BoolSort()) 
isPending = Function('isPending', Subject, BoolSort()) 
Paper = Function('Paper', Resource, BoolSort()) 
isEQPaper = Function('isEQPaper', Subject, Resource, BoolSort()) 
PaperSubmission = Function('PaperSubmission', Resource, BoolSort()) 
PaperDecision = Function('PaperDecision', Resource, BoolSort()) 
PaperConflicts = Function('PaperConflicts', Resource, BoolSort()) 
PaperAssignments = Function('PaperAssignments', Resource, BoolSort()) 
PaperReview = Function('PaperReview', Resource, BoolSort()) 
PaperReviewInfo = Function('PaperReviewInfo', Resource, BoolSort()) 
PaperReviewContent = Function('PaperReviewContent', Resource, BoolSort()) 
PaperReviewInfoSubmission = Function('PaperReviewInfoSubmissio', Resource, BoolSort()) 
MeetingFlag = Function('MeetingFlag', Resource, BoolSort()) 
isSubjectMeeting = Function('isSubjectMeeting', Subject, BoolSort()) 
isEQuserID = Function('isEQuserID', Subject, BoolSort()) 
isConflicted = Function('isConflicted', Subject, BoolSort()) 
isMeeting = Function('isMeeting', Subject, BoolSort()) 
isReviewInPlace = Function('isReviewInPlace', Subject, BoolSort()) 
                     
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
table.add_rule(And(PCmember(R), pcmember(X)), Pread(X, R)) # 7  TODO verifier 
# # # (![X, R] ((PcMember(R) & admin(X)) => (Pcreate(X, R) & Pwrite(X, R))))
table.add_rule(And(PCmember(R), admin(X)), And(Pcreate(X, R), Pwrite(X, R))) #8
# # # (![X, R] ((PcMember(R) & pcmember(X) & isEQuserID(X)) => ~PAnyAction(X, R)))
table.add_rule(And(PCmember(R), pcmember(X), isEQuserID(X)), Not(Paction(X, R))) # +9 
# # # (![X, R] ((PcMember(R) & admin(X)) => Pdelete(X, R)))
table.add_rule(And(PCmember(R), admin(X)), Pdelete(X, R)) #10
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

# ===============
size = 20 #47
for i in range(2, size):
    cumul = 0
    for j in range(10):
        start = clock()
        table.compute_table(i)
        #table.check(i) # 
        cumul +=  floor(clock()-start)
    # ---
    #print (str(i) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str(cumul/10))
    #print (str(i) + " time= " + str(cumul/10))
    print (str(cumul/10))
# # print (str(table))
# ===============
# # start = clock()
# size = 10
# table.compute_table(size)
# table.check() # !!! end < number_rules 
# # #table.checkExclu()
# # #table.checkSingleExclu()
# # print ("safe= " + str(len(table.exclusive)) + " time= " + str((clock()-start))) # +"\n" +str(table))
#  
# #table.perf("enumerative")
