__author__ = 'Andriu'

class Room:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return "Id: "+ str(self.name) + " type: " + str(self.type)