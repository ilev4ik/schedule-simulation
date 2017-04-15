from PyQt5 import Qt

class Worker(object):
    def __init__(self, fname, lname, dep, s):
        object.__init__(self)
        self.name = fname
        self.surname = lname
        self.department = dep
        self.state = s

    def switchState(self):
        states = [Qt.Checked, Qt.Unchecked]
        states.remove(self.state)
        self.state = states[0]

    def fullName(self):
        return self.name + ' ' + self.surname


class Department(object):
    def __init__(self, name, s):
        object.__init__(self)
        self.name = name
        self.state = s

    def switchState(self):
        states = [Qt.Checked, Qt.Unchecked]
        states.remove(self.state)
        self.state = states[0]


class Experiment(object):
    def __init__(self):
        pass


class ScheduleEvent(object):
    def __init__(self):
        pass