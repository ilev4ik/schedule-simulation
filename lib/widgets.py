from PyQt5.QtWidgets import \
    QWidget, QGroupBox, QVBoxLayout, \
    QLineEdit, QLayout, QComboBox, QFormLayout, \
    QSpinBox, QRadioButton, QCheckBox, QDialogButtonBox, QLabel
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import \
    QPainterPath, QRegion, QTransform

from .models import InfoTableView, InfoListView
from .models import DepartmentModel

# TODO: проверка на корректность
class FormWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        le_name = QLineEdit()
        cb_place = QComboBox()
        cb_place.addItems(['Конференц-зал', 'Помещение отдела', 'Столовая'])
        le_name.setPlaceholderText("Название мероприятия")

        vl_secInfo = QVBoxLayout()
        fl_duration = QFormLayout()

        sb_duration = QSpinBox()
        sb_duration.setRange(1, 8)
        fl_duration.addRow('Длительность (в ч.):', sb_duration)

        gb_participants = QGroupBox()
        gb_participants.setTitle('Участники')

        fl_participants = QFormLayout()
        # defs
        cb_department = QComboBox()
        cb_department.setModel(DepartmentModel(False))
        rb_department = QRadioButton('Отдел')
        rb_head = QRadioButton('Руководство')
        rb_workers = QRadioButton('Выбрать сотрудников')
        lw_workers = InfoTableView()

        fl_participants.addRow(rb_department, cb_department)
        fl_participants.addRow(rb_head)
        fl_participants.addRow(rb_workers)
        fl_participants.addRow(lw_workers)

        gb_participants.setLayout(fl_participants)

        vl_secInfo.addLayout(fl_duration)
        vl_secInfo.addWidget(gb_participants)

        bb_dialog = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        vl_secInfo.addWidget(bb_dialog)
        gb_secInfo = QGroupBox()

        gb_secInfo.setLayout(vl_secInfo)
        self.gb_secInfo = gb_secInfo
        layout = QVBoxLayout()
        layout.addWidget(le_name)
        layout.addWidget(cb_place)
        layout.addWidget(gb_secInfo)

        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.le_name = le_name
        self.cb_place = cb_place
        self.vl_secInfo = vl_secInfo
        self.sb_duration = sb_duration
        self.cb_department = cb_department
        self.rb_department = rb_department
        self.rb_head = rb_head
        self.rb_workers = rb_workers
        self.lw_workers = lw_workers

        self.setLayout(layout)
        self.__setDefaultState()
        rb_workers.clicked.connect(lw_workers.show)
        rb_department.clicked.connect(self.__onDeprtment)
        rb_head.clicked.connect(self.__onHead)
        rb_workers.clicked.connect(self.__onWorkers)

        bb_dialog.accepted.connect(gb_secInfo.hide)
        bb_dialog.rejected.connect(self.close)

        self.makeYellow()

    def resizeEvent(self, event):
        self.resize(self.sizeHint())
        path = QPainterPath()
        radius = 10
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon(QTransform()).toPolygon())
        self.setMask(mask)
        QWidget.resizeEvent(self, event)

    def __setDefaultState(self):
        self.le_name.clear()
        self.cb_place.setCurrentIndex(0)
        self.sb_duration.setValue(1)
        self.cb_department.setCurrentIndex(0)
        self.rb_department.setChecked(True)
        self.rb_head.setChecked(False)
        self.rb_workers.setChecked(False)
        self.lw_workers.hide()

    def __onDeprtment(self):
        self.cb_department.setEnabled(True)
        self.lw_workers.hide()

    def __onHead(self):
        self.cb_department.setEnabled(False)
        self.lw_workers.hide()

    def __onWorkers(self):
        self.cb_department.setEnabled(False)
        self.lw_workers.show()

    def showDescription(self):
        self.gb_secInfo.show()

    def makeWhite(self):
        self.setStyleSheet("background-color:white;")

    def makeRed(self):
        self.setStyleSheet("background-color:red;")

    def makeYellow(self):
        self.setStyleSheet("background-color:yellow;")


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
