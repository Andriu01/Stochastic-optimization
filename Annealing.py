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
Max_classes = 4
students = []
teachers = []
classes_names = ["A", "B","C", "D","E","F","G","H"]
classes = []



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
        for counter in xrange(Max_classes):
            while(True):
                activity = random_activity()
                if activity.teacher is None:
                    activity.teacher = teacher
                    activity.course = teacher.course
                    teacher.schedule.append(activity)
                    break
    #next add students each student mus have classes with each teacher
    for teacher in teachers:
        for student in students:
            while(True):
                activity = random_activity()
                class_teacher = activity.teacher
                if class_teacher:
                    class_teacher.students.append(student)
                    activity.students.append(student)
                    break
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
#todo check if all lectures has different
#return true if noe unique
def lecture_conflicts(Schedule):
    seen = set()
    return any(i.teacher in seen or seen.add(i.teacher) for i in Schedule)

#true if any student has conflict in this time
def students_conflicts(Schedule):
    sum= 0
    for Activity in Schedule:
        seen = set()
        count = 0
        #return any(s in seen or seen.add(s) for s in Activity.students)
        for students in Activity.students:
            if students in seen:
                count+=1
            else:
                seen.add(students)
        sum+= count
    return sum

    #return any(s in seen or seen.add(s) for s in i.students for i in Schedule)

#to improve
def calculate_cost():
    cost = 0
    for Day in Week:
        for Schedule in Day:
            conflict = lecture_conflicts(Schedule)
            if conflict:
                cost +=250
            students_with_conflict = students_conflicts(Schedule)
            if students_with_conflict:
                cost += 5*students_with_conflict
            #print conflict
            #for activity in Schedule:
             #   if activity.teacher is None:
              #      if activity.students:
               #         cost += 30*(len(activity.students))
             #   if len(activity.students) > 9:
             #       cost += 20*(len(activity.students)-10)
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



def swap_teacher(activity_a,activity_b):
    if activity_a.teacher != activity_b.teacher:
        activity_a.teacher,activity_b.teacher = activity_b.teacher ,activity_a.teacher
        activity_a.students,activity_b.students = activity_b.students ,activity_a.students

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
        activity_a = random_activity()
        activity_b = random_activity()
        swap_teacher(activity_a, activity_b)
        #activity_c = random_activity()
        #swapped = new_assignment(activity_c)
        #activity_a = random_activity()
        #if activity_a.teacher is None:
        #    if activity_a.students:
        #        for student in activity_a.students:
        #            while(True):
        #                new_activity = random_activity()
        #                if new_activity != activity_a:
        #                    if student not in new_activity.students:
        #                        new_activity.students.append(student)
        #                        break
        #        activity_a.students=[]
        #        swapped = True
        #activity_b = random_activity()
        # cannot swap if no student in activity
        #swapped = swap_two_students(activity_a,activity_b)
        swapped = True
        current_cost = calculate_cost()
        #swapped = False
        #print str(current_cost - solution_cost)
        if(current_cost > solution_cost):
            swapped = False
            swap_teacher(activity_b,activity_a)
        elif random.random()> probability(solution_cost,current_cost,temp):
            #only for swapping purpose
            #activity_a.students = copy_a
            #activity_b.students = copy_b
            swapped = False
            swap_teacher(activity_b,activity_a)
        if swapped:
            solution_cost=current_cost
            licznik = licznik + 1
            f.write(str(licznik) + " " + str(current_cost) + "\n")
        temp = cooling_temp(temp)
    print "Solution %d" % solution_cost
annealing(2000)
print_solution()