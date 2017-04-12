from PyQt5.QtWidgets import \
    QWidget, QGroupBox, QVBoxLayout, \
    QLineEdit, QLayout, QComboBox, QFormLayout, \
    QSpinBox, QRadioButton, QCheckBox, QDialogButtonBox, \
    QLabel, QTableView, QMenu, QAction, QAbstractItemView
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import \
    QPainterPath, QRegion, QTransform, QCursor, QContextMenuEvent

from .models import InfoTableView, InfoListView
from .models import DepartmentModel, CalendarModel


class ParametersWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        fl_parameters = QFormLayout()
        depInfo = InfoListView()
        period = QSpinBox()
        period.setRange(5,30)
        step = QComboBox()
        step.addItem('1 час')
        step.addItem('2 часа')
        defaultSchedule = QCheckBox()

        uplayout = QVBoxLayout()
        uplayout.addWidget(QLabel())
        uplayout.addWidget(depInfo)

        fl_parameters.addRow('Период моделирования', period)
        fl_parameters.addRow('Шаг моделирования', step)
        fl_parameters.addRow('Включить расписание по умолчанию', defaultSchedule)

        uplayout.addLayout(fl_parameters)
        gb_parameters = QGroupBox()
        gb_parameters.setTitle('Параметры моделирования')
        gb_parameters.setLayout(uplayout)

        self.depInfo = depInfo
        self.period = period
        self.step = step
        self.defaultSchedule = defaultSchedule

        layout = QVBoxLayout()
        layout.addWidget(gb_parameters)
        self.setLayout(layout)


class FilterWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        gb_filtering = QGroupBox()
        gb_filtering.setTitle('Параметры отображения')

        fl_filtering = QFormLayout()
        rb_firm = QRadioButton()
        rb_department = QRadioButton()
        rb_workers = QRadioButton()
        ilv_departments = InfoListView()
        itv_workers = InfoTableView()

        fl_filtering.addRow('Вся фирма', rb_firm)
        fl_filtering.addRow('Отделы для отображения', rb_department)
        fl_filtering.addRow(ilv_departments)
        fl_filtering.addRow('Сотрудники', rb_workers)
        fl_filtering.addRow(itv_workers)

        # self.fl_filtering = fl_filtering
        self.rb_firm = rb_firm
        self.rb_department = rb_department
        self.rb_workers = rb_workers
        self.ilv_departments = ilv_departments
        self.itv_workers = itv_workers

        gb_filtering.setLayout(fl_filtering)

        layout = QVBoxLayout()
        layout.addWidget(gb_filtering)

        self.__setDefaultState()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)
        rb_workers.clicked.connect(self.__onWorkers)
        rb_department.clicked.connect(self.__onDeprtment)
        rb_firm.clicked.connect(self.__onFirm)


    def __setDefaultState(self):
        self.rb_firm.setChecked(True)
        self.rb_workers.setChecked(False)
        self.rb_department.setChecked(False)
        self.ilv_departments.hide()
        self.itv_workers.hide()

    def __onDeprtment(self):
        self.ilv_departments.show()
        self.itv_workers.hide()

    def __onFirm(self):
        self.itv_workers.hide()
        self.ilv_departments.hide()

    def __onWorkers(self):
        self.itv_workers.show()
        self.ilv_departments.hide()


from lib.models import FormDelegate


class CalendarWidget(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.setModel(CalendarModel(12))
        self.setItemDelegate(FormDelegate())
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)

    def resizeEvent(self, event):
        w = self.viewport().width()
        h = self.viewport().height()
        for i in range(0, self.model().columnCount()):
            self.setColumnWidth(i, w / 7+1)

        for j in range(0, self.model().rowCount()):
            self.setRowHeight(j, h/9)

    def contextMenuEvent(self, event):
        QTableView.contextMenuEvent(self, event)
        e = QContextMenuEvent(event)
        self.menu = QMenu(self)
        action = QAction('Добавить событие', self)
        self.menu.addAction(action)
        self.menu.popup(QCursor.pos())
        action.triggered.connect(lambda: self.slot(e.pos()))

    def slot(self, pos):
        row = self.rowAt(pos.y())
        col = self.columnAt(pos.x())

        index = self.model().index(row, col)



