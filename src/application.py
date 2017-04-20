from PyQt5.QtCore import QObject
from .windows import MainWindow

from lib.entities import Department, Employee
from lib.logic_manager import LogicManager


class ScheduleSimulation(QObject):
    controller = LogicManager()

    def __init__(self):
        QObject.__init__(self)
        self.main_window = MainWindow()
        self.experiment_data = None

    def run(self):
        self.main_window.showMaximized()
