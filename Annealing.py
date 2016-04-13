import random
import math
from Teacher import Teacher
from Activity import Activity
from Student import Student
rooms = ["room1", "room2"]
Days_in_the_week = 5
Number_of_activities = 6
students = []
teachers = []

# init all
for i in xrange(100):
    students.append(Student("student_"+str(i)))
#Week = Week()
for i in xrange(4):
    teachers.append(Teacher("teacher_"+str(i),[],[]))
Week = []
#liczba dni tygodnia
for i in xrange(Days_in_the_week):
    day =[]
    #liczba mozliwych zajec
    for j in xrange(Number_of_activities):
        schedules = []
        for x in xrange(len(rooms)):
            Day_activity = Activity(rooms[x])
            schedules.append(Day_activity)
        day.append(schedules)
    Week.append(day)


def random_activity():
    day = random.randint(0, Days_in_the_week-1)
    termin = random.randint(0, Number_of_activities-1)
    room =random.randint(0, len(rooms)-1)
    activity = Week[day][termin][room]
    return activity

def print_activity(activity):
    print "&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    print "Room: %s" % activity.room
    print activity.students
    if activity.teacher:
        print "Teacher %s " % activity.teacher.name
        #print activity.teacher.students

def generate_random_solution():
    #first add teacher to lectures
    for teacher in teachers:
        for counter in xrange(teacher.max_classes):
            while(True):
                activity = random_activity()
                if activity.teacher is None:
                    activity.teacher = teacher
                    teacher.schedule.append(activity)
                    break
    #next add students each student mus have classes with each teacher
    for teacher in teachers:
        for student in students:
            activity = random_activity()
            class_teacher = activity.teacher
            if class_teacher:
                class_teacher.students.append(student)
            activity.students.append(student)

#generate_random_solution()
#print_activity(Week[0][0][0])

def print_solution():
    for Day in Week:
        print "################################"
        #liczba mozliwych zajec
        for Schedule in Day:
            print "--------------------------------------"
            for activity in Schedule:
                print_activity(activity)

#print_solution()

#to improve
def calculate_cost():
    cost = 0
    for Day in Week:
        for Schedule in Day:
            for activity in Schedule:
                if activity.teacher is None:
                    if activity.students:
                        cost += 30*(len(activity.students))
                if len(activity.students) > 9:
                    cost += 20*(len(activity.students)-10)
                #if not activity.students:
                #    if activity.teacher is None:
                #        cost -= 250
    return cost
#only change for now
def change_student_assignment():
    pass
def new_assignment(activity):
    swapped = False
    if activity.students:
        student_id = random.randint(0, (len(activity.students)-1))
        name = activity.students.pop(student_id)
        new_activity = random_activity()
        new_activity.students.append(name)
        swapped = True
    return swapped

#it doesnt change solution
def swap_two_students(activity_a,activity_b):
    swapped = False
    if bool(activity_a.students) and bool(activity_b.students):
        student_a_id = random.randint(0, (len(activity_a.students)-1))
        student_b_id = random.randint(0, (len(activity_b.students)-1))
        student_to_swap_a = activity_a.students[student_a_id]
        student_to_swap_b = activity_b.students[student_b_id]
        # Two different students
        if student_to_swap_a != student_to_swap_b:
            if student_to_swap_a not in activity_b.students:
                if student_to_swap_b not in activity_a.students:
                    copy_a = activity_a.students[:]
                    copy_b = activity_b.students[:]
                    name_a = activity_a.students.pop(student_a_id)
                    name_b = activity_b.students.pop(student_b_id)
                    activity_a.students.append(name_b)
                    activity_b.students.append(name_a)
                    #print_activity(activity_b)
                    swapped =True
    return swapped


def cooling_temp(temp):
    return temp * 0.99

#Boltzmann distribution
def probability(new_cost,cur_cost,temperatura):
    return math.exp(-((cur_cost-new_cost)/temperatura))

def annealing(temp):
    #generate
    f = open("tmp","wb")
    licznik = 0
    generate_random_solution()
    solution_cost = calculate_cost()
    print "Start with %d" % solution_cost
    while (temp > 0.01):
        #print temp
        activity_c = random_activity()
        swapped = new_assignment(activity_c)
        activity_a = random_activity()
        if activity_a.teacher is None:
            if activity_a.students:
                for student in activity_a.students:
                    while(True):
                        new_activity = random_activity()
                        if new_activity != activity_a:
                            if student not in new_activity.students:
                                new_activity.students.append(student)
                                break
                activity_a.students=[]
                swapped = True
        #activity_b = random_activity()
        # cannot swap if no student in activity
        #swapped = swap_two_students(activity_a,activity_b)
        current_cost = calculate_cost()
        #swapped = False
        #print str(current_cost - solution_cost)
        if(current_cost > solution_cost):
            swapped = False
        elif random.random()> probability(solution_cost,current_cost,temp):
            #only for swapping purpose
            #activity_a.students = copy_a
            #activity_b.students = copy_b
            swapped = False
        if swapped:
            solution_cost=current_cost
            licznik = licznik + 1
            f.write(str(licznik) + " " + str(current_cost) + "\n")
        temp = cooling_temp(temp)
    print "Solution %d" % solution_cost
annealing(2000)
print_solution()