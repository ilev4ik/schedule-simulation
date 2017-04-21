from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import QObject
from lib.entities import Calendar, ScheduleEvent

def show_error_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("This is a message box")
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle("MessageBox demo")
    msg.setDetailedText("The details are as follows:")
    msg.exec()

class LogicManager(QObject):
    @staticmethod
    def check_collisions(calendar: Calendar, new_event: ScheduleEvent):
        # обрати внимание, что new_event -- массив из одного элемента, иногда мб пустым по отмене
        print(calendar)
        print(new_event)
        show_error_message()
        return True

    # показываю как коммитить!!!!!!!!!
    # я вся внимание. ты в логике. никуда не переходи