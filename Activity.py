__author__ = 'Andriu'
from Teacher import *

class Activity:
    def __init__(self, room):
        self.room = room
        self.teacher = None
        self.students = []