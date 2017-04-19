from PyQt5.QtCore import QObject
from .windows import MainWindow

from lib.entities import Experiment, Department, Employee
from lib.logic_manager import LogicManager


class ScheduleSimulation(QObject):
    controller = LogicManager()

    def __init__(self):
        QObject.__init__(self)
        self.main_window = MainWindow()
        self.experiment_data = None

    def startExperiment(self):
        pass

    def nextStep(self):
        pass

    def pause(self):
        pass

    def resetExperiment(self):
        pass

    def finishExperiment(self):
        pass

    def setExperiment(self, new_experiment: Experiment):
        pass

    def run(self):
        self.main_window.showMaximized()
