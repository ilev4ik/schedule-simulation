from lib.entities import Calendar, ScheduleEvent


class LogicManager(object):
    @staticmethod
    def check_collisions(calendar: Calendar, new_event: ScheduleEvent):
        # обрати внимание, что new_event -- массив из одного элемента, иногда мб пустым по отмене
        print(calendar)
        print(new_event)
        return True