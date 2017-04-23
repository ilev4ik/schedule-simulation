from enum import Enum


class Human(object):
    def __init__(self, name: str, surname: str):
        self.__name= name
        self.__surname = surname

    def getName(self):
        return self.__name

    def getSurname(self):
        return self.__surname

    def getFullName(self):
        return self.__name + ' ' + self.__surname

    def __str__(self):
        return self.getFullName()


class Employee(Human):
    def __init__(self, name: str, surname: str):
        Human.__init__(self, name, surname)


class Department(object):
    def __init__(self, dep_name, boss=None, employee_list=None):
        object.__init__(self)
        if employee_list is None:
            employee_list = []

        self.__employee_list = employee_list
        self.__boss = boss
        self.__dep_name = dep_name

    def __str__(self):
        __str = []
        __str.append(self.__dep_name + ':')
        __str.append('Бос: ' + str(self.__boss))
        __str.append('Работники: ' + ', '.join([empl for empl in self.__employee_list]))
        return '\n'.join(__str) + '\n'

    def setBoss(self, new_boss: Employee):
        self.__boss = new_boss

    def addEmployee(self, employee: Employee):
        self.__employee_list.append(employee)

    def getName(self):
        return self.__dep_name

    def getEmployeeList(self):
        return self.__employee_list

    def getBoss(self):
        return self.__boss


class Firm(object):
    def __init__(self, boss: Human, dep_list=None):
        if dep_list is None:
            dep_list=[]
        self.__dep_list = dep_list
        self.__boss = boss

    def getBoss(self):
        return self.__boss


class ScheduleEvent(object):
    class Type(Enum):
        HEAD = 0
        DEP = 1
        EMPL = 2

    def __init__(self, **kwargs):
        self.__annotation = None
        self.__title = None
        self.__init_args(kwargs)

    def __init_args(self, kwargs: dict):
        for (key, value) in kwargs.items():
            if key is 'title':
                self.__title = value
            elif key is 'annotation':
                self.__annotation = value
            elif key is 'day':
                self.__day = value
            elif key is 'time':
                self.__time = value
            elif key is 'duration':
                self.__duration = value
            elif key is 'location':
                self.__location = value
            elif key is 'type':
                self.__type = value
            elif key is 'part_list':
                self.__part_list = value
            else:
                raise KeyError(key)

    def getTitle(self):
        return self.__title

    def getAnnotation(self):
        return self.__annotation

    def getDuration(self):
        return self.__duration

    def getLocation(self):
        return self.__location

    def getType(self):
        return self.__type

    def getDay(self):
        return self.__day

    def getTime(self):
        return self.__time

    def getPartList(self):
        return self.__part_list


class Calendar(object):
    def __init__(self, matrix):
        self.currentTime = 0.0
        self.matrix = matrix
        self.period = len(matrix[0])
