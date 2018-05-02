# -------------------
# 30/4/2018
# Test ArtOfProlog 
# -------------------
### program-2.2 Program 2.2: A circuit for a logical and-gate
### May be problem with Room is it Location related ?

from Sorting import * #@UnusedWildImport
from time import * #@UnusedWildImport

# --------------------------
Professor = DeclareSort('Professor')
Lecture = DeclareSort('Lecture')
Duration = DeclareSort('Duration')
Place = DeclareSort('Place')
Date = DeclareSort('Date')

table = Sorting()
# Variables
table.add_variable("Lecturer", Professor)
table.add_variable("Course", Lecture)
table.add_variable("Time", IntSort()) ## simplif
table.add_variable("Location", Place)
table.add_variable("Day", Date)
table.add_variable("Start", IntSort())
table.add_variable("Finish", IntSort())
table.add_variable("Length", IntSort())
table.add_variable("Room", Place) ### doubt about that
Lecturer = table.get_variable(0)
Course = table.get_variable(1)
Time = table.get_variable(2)
Location = table.get_variable(3)
Day = table.get_variable(4)
Start = table.get_variable(5)
Finish = table.get_variable(6)
Length = table.get_variable(7)
Room = table.get_variable(8)

#  predicates 
lecturer = Function('lecturer', Professor, Lecture, BoolSort()) 
course = Function('course', Lecture, IntSort(), Professor, Place, BoolSort()) 
time = Function('time', Date, IntSort(), IntSort(), IntSort()) 
##plus = Function('plus', IntSort(), IntSort(), IntSort(), IntSort())  ### is it addition ?
duration = Function('duration', Lecture, IntSort(), BoolSort()) 
teaches = Function('teaches', Professor, Date, BoolSort()) 
occupied = Function('occupied', Place, Date, IntSort(), BoolSort()) 

#    lecturer(Lecturer,Course) :-        course(Course,Time,Lecturer,Location).
table.add_rule(course(Course,Time,Lecturer,Location), lecturer(Lecturer,Course))
#    duration(Course,Length) :-        course(Course,time(Day,Start,Finish),Lecturer,Location),         plus(Start,Length,Finish).
table.add_rule(And(course(Course, time(Day,Start,Finish), Lecturer, Location), ((Start + Length) == Finish)), duration(Course,Length))
#    teaches(Lecturer,Day) :-         course(Course,time(Day,Start,Finish),Lecturer,Location).
table.add_rule(course(Course, time(Day,Start,Finish), Lecturer, Location), teaches(Lecturer,Day))
### strange no Room relation ? is it a location ?
#    occupied(Room,Day,Time) :-         course(Course,time(Day,Start,Finish),Lecturer,Location),         Start =< Time, Time =< Finish.
table.add_rule(And(course(Course, time(Day, Start, Finish), Lecturer, Location), (Start <= Time), (Time <= Finish)), occupied(Room, Day, Time))
### rules= 4 safe= 9 unsafe= 0 time= 1

#### =====================
start = clock()
table.compute_table(4)
table.check()
print ("rules= " + str(len(table.correct)) + " safe= " + str(len(table.safe)) + " unsafe= " + str(len(table.unsafe)) + " time= " + str(floor(clock()-start)))
print (str(table))
### print(str(table.get_safe_conditions()))
#table.quine()
#table.perf("test")
