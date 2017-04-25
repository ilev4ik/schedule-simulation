from PyQt5.QtWidgets import QMessageBox
from lib.entities import Calendar, ScheduleEvent

def show_error_message(event: ScheduleEvent):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Ошибка")
    msg.setInformativeText("Коллизия события: " + event.getTitle())
    msg.setWindowTitle("Коллизия")
    msg.setDetailedText("Поменяйте время этого события или исключите его из календаря")
    msg.exec()


class LogicManager(object):
    @staticmethod
    def check_collisions(calendar: Calendar, new_event):
        if new_event:
            show_error_message(new_event)
        return True

    @staticmethod
    def simulate_next_step(calendar: Calendar, step, current_cell: dict):
        """
        
        :param calendar of type Calendar
        :param step 1 or 2
        :param current_cell of type dict : {'row': i, 'col': j} where i, j are ints 
        :return an array of [rest_events_number, next_cell]. Next cell has format of current_cell
        if rest_event_number equals 0 then next_cell = None
        """
        return 1, {'row': 5, 'col': 2}