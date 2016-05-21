__author__ = 'Andriu'

class Teacher:
    def __init__(self,name, students,schedule, course):
        self.name = name
        self.students = students
        self.course = course
        self.schedule = schedule
        # how many classes
        self.classes = 0