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
        total_day_num = calendar.period
        current_day_num = current_cell['col'] + 1
        current_time = current_cell['row'] + step

        if current_time + 1 <= 9:
            current_cell['row'] += step
        else:
            if current_day_num + 1 <= total_day_num:
                current_cell['col'] += 1
                current_cell['row'] = 0
            else:
                return 0, None
        events_left = 0
        # здесь подсчёт оставшихся событий
        for day_idx in range(current_cell['col'], total_day_num):
            if day_idx == current_cell['col']:
                start_time = current_cell['row']
            else:
                start_time = 0
            for time_idx in range(start_time, 9, 1):
                events_now = len(calendar.matrix[time_idx][day_idx])
                events_left += events_now

        return events_left, current_cell
