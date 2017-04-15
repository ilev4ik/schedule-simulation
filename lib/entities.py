from PyQt5.Qt import *

class Worker(object):
    def __init__(self, fname, lname, dep):
        object.__init__(self)
        self.name = fname
        self.surname = lname
        self.department = dep



    def fullName(self):
        return self.name + ' ' + self.surname


class Department(object):
    def __init__(self, name):
        object.__init__(self)
        self.name = name


class Experiment(object):
    def __init__(self):
        pass


class ScheduleEvent(object):
    def __init__(self):
        pass