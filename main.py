from sys import argv
from PyQt5.QtWidgets import QApplication

from src.application import ScheduleSimulation


import resources

if __name__ == '__main__':
    app = QApplication(argv)
    schedule = ScheduleSimulation()
    schedule.run()

    app.exec()