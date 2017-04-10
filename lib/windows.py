from PyQt5.QtWidgets import QMainWindow, QDockWidget, QStackedWidget
from lib.widgets import FormWidget, ParametersWidget, FilterWidget

from PyQt5.Qt import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        params = QDockWidget()
        params.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        params.setWidget(ParametersWidget())
        self.addDockWidget(Qt.LeftDockWidgetArea, params)

        filter = QDockWidget()
        filter.setAllowedAreas(Qt.RightDockWidgetArea)
        filter.setWidget(FilterWidget())
        self.addDockWidget(Qt.RightDockWidgetArea, filter)

        console = QDockWidget()
        console.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        console.setWidget(QStackedWidget())
        self.addDockWidget(Qt.BottomDockWidgetArea, console)

        self.setCentralWidget(FormWidget())
