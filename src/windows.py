from lib.widgets import ParametersWidget, FilterWidget, CalendarWidget

from PyQt5.Qt import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Симулятор офисного расписания')
        params = QDockWidget()
        params.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        params.setWidget(ParametersWidget())
        self.addDockWidget(Qt.LeftDockWidgetArea, params)

        filter = QDockWidget()
        filter.setAllowedAreas(Qt.RightDockWidgetArea)
        filter.setWidget(FilterWidget())
        self.addDockWidget(Qt.RightDockWidgetArea, filter)

        console = QDockWidget()
        console.setAllowedAreas(Qt.BottomDockWidgetArea)

        tabs = QTabWidget()

        # scroll to bottom
        confWidget = QListWidget()
        confWidget.model().rowsInserted.connect(confWidget.scrollToBottom)
        tabs.addTab(confWidget, "Конфигурация")
        tabs.addTab(QListWidget(), "Вывод")
        tabs.addTab(QListWidget(), "Ошибки")

        console.setWidget(tabs)
        self.tabs = tabs
        self.addDockWidget(Qt.BottomDockWidgetArea, console)

        self.setCentralWidget(CalendarWidget(self))

        self.__createActions()
        self.__createMenus()
        self.__createToolBars()

    def __createActions(self):
        newAction = QAction('&Повторить', self)
        newAction.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        newAction.setShortcut(QKeySequence.Forward)
        newAction.setStatusTip('Повторить моделирование')
        newAction.triggered.connect(lambda: self.tabs.widget(0).addItem('Повторить моделирование'))
        self.newAction = newAction

        finishAction = QAction('&Завершить моделирование', self)
        finishAction.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        finishAction.setShortcut(Qt.Key_Space)
        finishAction.setStatusTip('Завершить моделирование')
        finishAction.triggered.connect(lambda: self.tabs.widget(0).addItem('Завершить моделирование'))
        self.finishAction = finishAction

        cancelAction = QAction('&Сбросить', self)
        cancelAction.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
        cancelAction.setShortcut(Qt.Key_Stop)
        cancelAction.setStatusTip('Сброс параметров моделирования')
        cancelAction.triggered.connect(lambda: self.tabs.widget(0).addItem('Сброс параметров моделирования'))
        self.cancelAction = cancelAction

        nextAction = QAction('&Следующий шаг', self)
        nextAction.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        nextAction.setShortcut(QKeySequence.Forward)
        nextAction.setStatusTip('Следующий шаг моделирования')
        nextAction.triggered.connect(lambda: self.tabs.widget(0).addItem('Следующий шаг моделирования'))
        self.nextAction = nextAction

        startAction = QAction('&Начать', self)
        startAction.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        startAction.setShortcut(Qt.Key_Stop)
        startAction.setStatusTip('Начало моделирования')
        startAction.triggered.connect(lambda: self.tabs.widget(0).addItem('Начало моделирования'))
        self.startAction = startAction

        pauseAction = QAction('&Пауза', self)
        pauseAction.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        pauseAction.setShortcut(Qt.Key_Pause)
        pauseAction.setStatusTip('Пауза моделирования')
        pauseAction.triggered.connect(lambda: self.tabs.widget(0).addItem('Пауза моделирования'))
        self.pauseAction = pauseAction

        exitAction = QAction('&Выход', self)
        exitAction.setShortcut(Qt.Key_Exit)
        exitAction.setStatusTip('Выход')
        exitAction.triggered.connect(self.close)
        self.exitAction = exitAction


    def __createMenus(self):
        sessionMenu = self.menuBar().addMenu('Сессия')
        sessionMenu.addAction(self.newAction)
        sessionMenu.addAction(self.cancelAction)
        sessionMenu.addSeparator()
        sessionMenu.addAction(self.exitAction)

        controlMenu = self.menuBar().addMenu('Управление')
        controlMenu.addAction(self.startAction)
        controlMenu.addAction(self.pauseAction)
        controlMenu.addAction(self.nextAction)
        controlMenu.addAction(self.finishAction)

    def __createToolBars(self):
        sessioToolBar = self.addToolBar('Сессия')
        sessioToolBar.addAction(self.newAction)
        sessioToolBar.addAction(self.cancelAction)

        controlToolBar = self.addToolBar('Управление')
        controlToolBar.addAction(self.startAction)
        controlToolBar.addAction(self.pauseAction)
        controlToolBar.addAction(self.nextAction)
        controlToolBar.addAction(self.finishAction)
