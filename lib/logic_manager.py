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