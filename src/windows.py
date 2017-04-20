from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QFile, QIODevice, QTextStream
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTabWidget, \
    QListWidget, QAction, QStyle
from PyQt5.QtGui import QKeySequence

from lib.widgets import ParametersWidget, FilterWidget, CalendarWidget, FormDialog
from lib.entities import Department, Employee, ScheduleEvent, Firm, Human


class MainWindow(QMainWindow):
    dep_file_name_list = [
        'analytics', 'bookkeeping', 'development',
        'finances', 'hr', 'marketing', 'purchasing',
        'sales', 'testing'
    ]

    dep_name_list = [
        'Аналитический отдел',
        'Бухгалтерия',
        'Отдел закупок',
        'Отдел кадров',
        'Отдел маркетинга',
        'Отдел разработки',
        'Отдел продаж',
        'Отдел тестирования',
        'Финансовый отдел'
    ]

    def __init__(self):
        QMainWindow.__init__(self)
        MainWindow.departments_committed = pyqtSignal(list)

        data = self.__readDepartmentsData()
        self.firm = Firm(Human('Иван', 'Попов'), data)

        self.setWindowTitle('Симулятор офисного расписания')

        # parameters
        self.params_dock = QDockWidget()
        self.params_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.params_widget = ParametersWidget(data)
        self.params_dock.setWidget(self.params_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.params_dock)

        # filter
        self.filter_dock = QDockWidget()
        self.filter_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # console
        console = QDockWidget()
        console.setAllowedAreas(Qt.BottomDockWidgetArea)

        # tabs
        tabs = QTabWidget()
        confWidget = QListWidget()
        confWidget.model().rowsInserted.connect(confWidget.scrollToBottom)
        tabs.addTab(confWidget, "История")
        console.setWidget(tabs)
        self.addDockWidget(Qt.BottomDockWidgetArea, console)

        # Calendar
        init_matrix = [[[] for i in range(0, 7)] for j in range(0, 9)]
        self.calendar = CalendarWidget(7, init_matrix, self)
        self.setCentralWidget(self.calendar)

        self.tabs = tabs

        self.__createActions()
        self.__setDefaultState()

        self.__createMenus()
        self.__createToolBars()

    def __setDefaultState(self):
        self.params_dock.widget().getModel().uncheckAll()
        self.params_dock.setEnabled(True)
        self.startAction.setEnabled(True)
        self.newAction.setEnabled(False)
        self.pauseAction.setEnabled(False)
        self.cancelAction.setEnabled(False)
        self.nextAction.setEnabled(False)
        self.finishAction.setEnabled(False)
        self.centralWidget().setEnabled(False)
        self.filter_dock.hide()

    def __clearCalendar(self):
        pass

    def __onCancelAction(self):
        self.tabs.widget(0).addItem('Сбросить параметры моделирования')
        self.__setDefaultState()

    def __onResetAction(self):
        self.tabs.widget(0).addItem('Очистить календарь')

    def __onPauseAction(self):
        self.tabs.widget(0).addItem('Пауза моделирования')

    def __onStartAction(self):
        checked_departments = self.params_widget.getModel().getCheckedDepartmentList()
        self.checked_departments = checked_departments
        if len(checked_departments) == 0:
            self.tabs.widget(0).addItem('Ошибка [параметры]: выберите хотя бы один отдел')
            return
        num_of_days = self.params_widget.sb_period.value()
        self.Matrix = [[[] for i in range(0, num_of_days)] for j in range(0, 9)]

        if self.params_widget.chb_defaultSchedule.isChecked():
            self.__readDefaultSchedule(num_of_days)

        self.filter_dock.setWidget(FilterWidget(checked_departments))
        self.calendar = CalendarWidget(num_of_days, self.Matrix, self)
        self.calendar.setFormData(checked_departments)
        self.setCentralWidget(self.calendar)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filter_dock)
        self.params_dock.setEnabled(False)
        self.newAction.setEnabled(True)
        self.cancelAction.setEnabled(True)
        self.nextAction.setEnabled(True)
        self.finishAction.setEnabled(True)
        self.tabs.widget(0).addItem('Начало моделирования')
        self.startAction.setEnabled(False)
        self.pauseAction.setEnabled(False)
        self.filter_dock.show()

    def __onNextAction(self):
        self.tabs.widget(0).addItem('Следующий шаг')

    def __onFinishAction(self):
        self.tabs.widget(0).addItem('Завершить моделирование')

    def __createActions(self):
        newAction = QAction('&Очистить календарь', self)
        newAction.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        newAction.setShortcut(QKeySequence.Forward)
        newAction.setStatusTip('Очистить календарь')
        newAction.triggered.connect(self.__onResetAction)
        self.newAction = newAction

        cancelAction = QAction('&Сбросить параметры моделирования', self)
        cancelAction.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
        cancelAction.setShortcut(Qt.Key_Stop)
        cancelAction.setStatusTip('Сбросить параметры моделирования')
        self.cancelAction = cancelAction
        self.cancelAction.triggered.connect(self.__onCancelAction)

        startAction = QAction('&Начать', self)
        startAction.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        startAction.setShortcut(Qt.Key_Stop)
        startAction.setStatusTip('Начало моделирования')
        startAction.triggered.connect(self.__onStartAction)
        self.startAction = startAction

        nextAction = QAction('&Следующий шаг', self)
        nextAction.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        nextAction.setShortcut(Qt.Key_Space)
        nextAction.setStatusTip('Следующий шаг')
        nextAction.triggered.connect(self.__onNextAction)
        self.nextAction = nextAction

        finishAction = QAction('&Завершить моделирование', self)
        finishAction.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        finishAction.setShortcut(QKeySequence.Forward)
        finishAction.setStatusTip('Завершить моделирование')
        finishAction.triggered.connect(self.__onFinishAction)
        self.finishAction = finishAction

        pauseAction = QAction('&Пауза', self)
        pauseAction.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        pauseAction.setShortcut(Qt.Key_Pause)
        pauseAction.setStatusTip('Пауза моделирования')
        pauseAction.triggered.connect(self.__onPauseAction)
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
        controlToolBar.addAction(self.nextAction)
        controlToolBar.addAction(self.finishAction)
        controlToolBar.addAction(self.pauseAction)

    def __readDefaultSchedule(self, num_of_days):
        file_name = 'default'
        file = QFile(':/schedule/' + file_name + '.txt')

        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            raise FileNotFoundError(file_name)

        stream = QTextStream(file)
        stream.setCodec('UTF-8')

        Matrix = [[[] for i in range(0, num_of_days)] for j in range(0, 9)]
        days_of_week = ['', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        while not stream.atEnd():
            week_day = stream.readLine()[:-1]
            line = stream.readLine()
            while line:
                params_of_event = line.split(',')
                time = int(params_of_event[0].replace(':', ''))
                duration = int(params_of_event[1])
                title = params_of_event[2]
                location = params_of_event[3]
                department = params_of_event[4]
                start_day_number = days_of_week.index(week_day)
                days_list = [k for k in range(start_day_number, num_of_days, 7)]

                type = ScheduleEvent.Type.HEAD if department == 'Руководство' else ScheduleEvent.Type.DEP
                participants_list = []
                if type == ScheduleEvent.Type.HEAD:
                    participants_list.append(self.firm.getBoss())
                    for dep in self.checked_departments:
                        participants_list.append(dep.getBoss())
                elif type == ScheduleEvent.Type.DEP:
                    for dep in self.checked_departments:
                        if dep.getName() == department:
                            participants_list.extend(dep.getEmployeeList())
                else:
                    raise Exception('Error while processing default schedule data: TYPE')

                for day in days_list:
                    if len(participants_list) != 0:
                        Matrix[int(time/100)-10][day-1].append(ScheduleEvent(time=time,
                                                               duration=duration,
                                                               title=title,
                                                               location=location,
                                                               type=type,
                                                               part_list=participants_list,
                                                               day=day
                                                               )
                                                 )
                line = stream.readLine()

        self.Matrix = Matrix

    def __readDepartmentsData(self):
        department_list = []  # of Department
        for file_name in MainWindow.dep_file_name_list:
            count = 0
            file = QFile(':/stuff/' + file_name + '.txt')
            if not file.open(QIODevice.ReadOnly | QIODevice.Text):
                raise FileNotFoundError(file_name)

            stream = QTextStream(file)
            stream.setCodec('UTF-8')
            dep_name = stream.readLine()
            if dep_name[-1] != ':':
                raise Exception('resource ' + file_name + ' with no department mark')

            dep_name = dep_name[:-1]
            new_dep_obj = Department(dep_name)

            while not stream.atEnd():
                count += 1
                (n, s) = stream.readLine().split()
                if count == 1:
                    new_dep_obj.setBoss(Employee(n, s))
                else:
                    new_dep_obj.addEmployee(Employee(n, s))

            if count == 0:
                raise Exception('resource ' + file_name + ' has no items')

            department_list.append(new_dep_obj)
        return department_list