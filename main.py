from sys import argv
from PyQt5.QtWidgets import QApplication

from src.application import ScheduleSimulation
from lib.logic_manager import LogicManager
import resources

if __name__ == '__main__':
    app = QApplication(argv)
    schedule = ScheduleSimulation()
    schedule.run()
    LogicManager.custom_print(1)
    app.exec()