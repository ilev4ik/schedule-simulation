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
    def check_collisions(calendar: Calendar, new_event):
        # обрати внимание, что new_event -- массив из одного элемента, иногда мб пустым по отмене
        # print(calendar)
        print(new_event)

        if new_event == []:
            return True
        for event in new_event:
            if event == []:
                continue
            else:
                # обрабатываем событие
                day = event.getDay()
                time = int(event.getTime()/100-10)
                print(calendar.matrix[time][day])
                print('111')
                set_events_list = calendar.matrix[time][day]
                for elem in set_events_list:
                    if elem == []:
                        set_events_list.remove(elem)

                print('222')
                print(set_events_list)

                if set_events_list == []:
                    print('***')
                    print(new_event)
                    return True
                print('333')
                titles_list = [ev.getTitle() for ev in set_events_list]
                print('444')
                print(titles_list)
                print('555')


        # if len(new_event) == 0:
        #     return True
        # if new_event[0].getTitle() == '123':
        #     show_error_message()
        #     return False
        return True
