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
        total_day_num = calendar.period
        current_day_num = current_cell['col'] + 1
        current_time = current_cell['row'] + 1

        if current_time + 1 <= 9:
            current_cell['row'] += 1
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

    """
        days = calendar.period
        hours = 9

        new_day = current_cell['col']
        new_time = current_cell['row'] + step

        if new_day > days-1:
            return 0, None
        else:
            new_cell = {'row': new_time, 'col': new_day}

        # переход на след день
        if new_time > 8:
            new_time = 0
            new_day += 1

        events_left = 0


"""