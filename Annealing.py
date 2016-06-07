import random
import math
from Teacher import Teacher
from Activity import Activity
from Student import Student
from Room import Room
from Course import Course
rooms = []
Days_in_the_week = 5
Number_of_activities = 6
Max_classes = 5
students = []
teachers = []
classes_names = ["A", "B","C", "D","E","F","G","H"]
classes = []

# 100 students 1 lecture

for i in classes_names:
    classes.append((Course(i)))
#todo przedmioty oraz wiecej prowadzacych

for i in xrange(2):
    rooms.append(Room("room"+str(i),"LAB"))
rooms.append(Room("room100","LECTURE"))
# init all
for i in xrange(100):
    students.append(Student("student_"+str(i)))
#Week = Week()
for i in xrange(len(classes)):
    teachers.append(Teacher("teacher_"+str(i),[],[],classes[i]))
    #teachers.append(Teacher("teacher_1"+str(i),[],[],Lectures[i]))
Week = []
#liczba dni tygodnia
for i in xrange(Days_in_the_week):
    day =[]
    #liczba mozliwych zajec
    for j in xrange(Number_of_activities):
        schedules = []
        for room in rooms:
            Day_activity = Activity(room)
            schedules.append(Day_activity)
        day.append(schedules)
    Week.append(day)


def random_activity(type):

    match = False
    day = random.randint(0, Days_in_the_week-1)
    termin = random.randint(0, Number_of_activities-1)
    room =random.randint(0, len(rooms)-1)
    activity = Week[day][termin][room]
    if activity.room.type == type:
        match = True
    return (match,activity)

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
        for counter in xrange(Max_classes):
            type = "LAB"
            while(True):
                match, activity = random_activity(type)
                if match and activity.teacher is None:
                    activity.teacher = teacher
                    teacher.schedule.append(activity)
                    #activity.course = teacher.course
                    teacher.course.activities.append(activity)
                    break
        #add foreach teacher 1 lecture with all students
        type = "LECTURE"
        while(True):
            match, activity = random_activity(type)
            if match and activity.teacher is None:
                for ident in xrange(len(students)):
                    activity.students.append(students[ident])
                activity.teacher = teacher
                #teacher.schedule.append(activity)
                #activity.course = teacher.course
                #teacher.course.activities.append(activity)
                break
            #print "Next TRY"
    #next add students each student mus have classes with each teacher
    for teacher in teachers:
        #print(teacher.course.activity)
        for ident in xrange(len(students)):
            added_activity= teacher.schedule[ident/20]
            #for j in xrange(20):
            added_activity.students.append(students[ident])
            teacher.students.append(students[ident])
            teacher.course.students.append(students[ident])

def print_solution():
    for Day in Week:
        print "################################"
        #liczba mozliwych zajec
        for Schedule in Day:
            print "--------------------------------------"
            for activity in Schedule:
                print_activity(activity)

def teacher_conflicts(Schedule):
    seen = set()
    for activity in Schedule:
        if activity.teacher in seen:
            return True
        elif activity.teacher:
            seen.add(activity.teacher)
    return False

#true if any student has conflict in this time
def students_conflicts(Schedule):
    sum= 0
    for Activity in Schedule:
        seen = set()
        count = 0
        for students in Activity.students:
            if students in seen:
                count+=1
            else:
                seen.add(students)
        sum+= count
    return sum

def lecture_conflicts(Schedule):

    counter = 0
    lecture = False
    for activity in Schedule:
        if activity.room.type=="LAB" and activity.teacher:
            counter +=1
        if activity.room.type=="LECTURE" and activity.teacher:
            lecture = True
    if lecture:
        return counter != 0
    else:
        return False

#to improve
def calculate_cost():
    cost = 0
    for Day in Week:
        for Schedule in Day:
            conflict = lecture_conflicts(Schedule)
            if conflict:
                cost += 250
            conflict = teacher_conflicts(Schedule)
            if conflict:
                cost += 100
            #students_with_conflict = students_conflicts(Schedule)
            #if students_with_conflict:
            #    cost += 5*students_with_conflict
    return cost

#only change for now
def change_student_assignment(classes):
    ind_1, ind_2 = random.sample(range(0, (len(classes.activities)-1)),2)
    activity_a = classes.activities[ind_1]
    activity_b = classes.activities[ind_2]
    while(True):
        student_a_ind = random.randint(0, (len(activity_a.students)-1))
        student_b_ind = random.randint(0, (len(activity_b.students)-1))
        if activity_a.students[student_a_ind].name != activity_b.students[student_b_ind].name:
            swap_students(activity_a, student_a_ind,activity_b, student_b_ind)
            break
    return [activity_a,student_a_ind,activity_b,student_b_ind]

def new_assignment(activity):
    swapped = False
    if activity.students:
        student_id = random.randint(0, (len(activity.students)-1))
        name = activity.students.pop(student_id)
        match, new_activity = random_activity("LAB")
        if match:
            new_activity.students.append(name)
            swapped = True
    return swapped

def swap_students(activity_a, student_a_ind,activity_b, student_b_ind):
    student_a= activity_a.students.pop(student_a_ind)
    student_b= activity_b.students.pop(student_b_ind)
    activity_a.students.append(student_b)
    activity_b.students.append(student_a)

def swap_teacher(activity_a,activity_b):
    teacher_a = activity_a.teacher
    teacher_b = activity_b.teacher
    #print(teacher_a)
    #print(teacher_b)
    if teacher_a is None or teacher_b is None:
        return False
    if teacher_a != teacher_b:
        activity_a.teacher,activity_b.teacher = activity_b.teacher ,activity_a.teacher
        activity_a.students,activity_b.students = activity_b.students ,activity_a.students
        teacher_a.schedule.remove(activity_a)
        teacher_a.schedule.append(activity_b)
        teacher_a.course.activities.remove(activity_a)
        teacher_a.course.activities.append(activity_b)
        teacher_b.schedule.remove(activity_b)
        teacher_b.schedule.append(activity_a)
        teacher_b.course.activities.remove(activity_b)
        teacher_b.course.activities.append(activity_a)
        return True
    return False

def new_teacher_assignment(teacher, old_activity, new_activity):


    new_activity.students = old_activity.students
    new_activity.teacher = teacher
    old_activity.students = []
    old_activity.teacher = None
    teacher.schedule.remove(old_activity)
    teacher.schedule.append(new_activity)
    teacher.course.activities.remove(old_activity)
    teacher.course.activities.append(new_activity)


def cooling_temp(temp):
    return temp * 0.99

#Boltzmann distribution
def probability(new_cost,cur_cost,temperatura):
    return math.exp(-((cur_cost-new_cost)/temperatura))

# dodac liste uczniow na danym przedmiocie i random zmiany w jego obrebie

def annealing(temp):
    f = open("tmp","wb")
    licznik = 0
    generate_random_solution()
    print "First Solution"
    #print_solution()
    solution_cost = calculate_cost()
    print "Start with %d" % solution_cost
    while (temp > 0.01):

        while(True):
            match_a, activity_a = random_activity("LAB")
            match_b, activity_b = random_activity("LAB")
            if (match_a and match_b):
                break
        swapped= swap_teacher(activity_a, activity_b)

        class_to_swap = classes[random.randint(0, len(classes)-1)]
        changes = change_student_assignment(class_to_swap)

        teacher = teachers[random.randint(0, len(teachers)-1)]
        while(True):
            match, new_activity = random_activity("LAB")
            if match and new_activity.teacher is None:
                break
        old_activity = teacher.schedule[random.randint(0, Max_classes-1)]
        new_teacher_assignment(teacher, old_activity, new_activity)
        current_cost = calculate_cost()
        swapped = True
        if(current_cost > solution_cost):
            swapped = False
            new_teacher_assignment(teacher, new_activity, old_activity)
            swap_teacher(activity_b,activity_a)
            swap_students(changes[0], changes[3],changes[2], changes[1])
        elif random.random()> probability(solution_cost,current_cost,temp):
            swapped = False
            new_teacher_assignment(teacher, new_activity, old_activity)
            swap_teacher(activity_b,activity_a)
            swap_students(changes[0], changes[3],changes[2], changes[1])
        if swapped:
            solution_cost=current_cost
            licznik = licznik + 1
        f.write(str(licznik) + " " + str(current_cost) + "\n")
        temp = cooling_temp(temp)
    print "Solution %d" % solution_cost



annealing(1000)
print_solution()
#for corse in classes:
#    print corse.activity[0].students
#    print len(corse.students)