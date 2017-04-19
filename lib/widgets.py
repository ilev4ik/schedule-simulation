from PyQt5.Qt import *

from PyQt5.QtWidgets import \
    QWidget, QGroupBox, QVBoxLayout, \
    QLineEdit, QLayout, QComboBox, QFormLayout, \
    QSpinBox, QRadioButton, QCheckBox, QDialogButtonBox, \
    QLabel, QTableView, QAbstractItemView, QMenu, QAction, \
    QGridLayout, QPushButton, QSizePolicy, QDialog, QTextEdit, \
    QStyledItemDelegate
from PyQt5.QtCore import QRectF, QRect, QPoint
from PyQt5.QtGui import \
    QPainterPath, QRegion, QTransform, QContextMenuEvent, \
    QIcon
from PyQt5.QtGui import QCursor
from PyQt5.Qt import pyqtSignal

from .views import InfoTableView, InfoListView
from .models import DepartmentModel, CalendarModel, WorkersModel

from .entities import Department


class ParametersWidget(QWidget):
    def __init__(self, department_list: [Department]):
        QWidget.__init__(self)
        fl_parameters = QFormLayout()
        depInfo = InfoListView(DepartmentModel(department_list))
        sb_period = QSpinBox()
        sb_period.setRange(7,30)
        cb_step = QComboBox()
        cb_step.addItem('1 час')
        cb_step.addItem('2 часа')
        chb_defaultSchedule = QCheckBox()

        uplayout = QVBoxLayout()
        uplayout.addWidget(QLabel())
        uplayout.addWidget(depInfo)

        fl_parameters.addRow('Период моделирования (дн.):', sb_period)
        fl_parameters.addRow('Шаг моделирования (ч.):', cb_step)
        fl_parameters.addRow('Включить расписание по умолчанию', chb_defaultSchedule)

        uplayout.addLayout(fl_parameters)
        gb_parameters = QGroupBox()
        gb_parameters.setTitle('Параметры моделирования')
        gb_parameters.setLayout(uplayout)

        self.depInfo = depInfo
        self.sb_period = sb_period
        self.cb_step = cb_step
        self.chb_defaultSchedule = chb_defaultSchedule

        layout = QVBoxLayout()
        layout.addWidget(gb_parameters)
        self.setLayout(layout)

    def getModel(self):
        return self.depInfo.model()


class FilterWidget(QWidget):
    def __init__(self, department_list: list):
        QWidget.__init__(self)
        gb_filtering = QGroupBox()
        gb_filtering.setTitle('Параметры отображения')

        fl_filtering = QFormLayout()
        rb_firm = QRadioButton()
        rb_department = QRadioButton()
        rb_workers = QRadioButton()

        ilv_departments = InfoListView(DepartmentModel(department_list, Qt.Checked))
        itv_workers = InfoTableView(WorkersModel(department_list))

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

    def getModel(self):
        return self.itv_workers.model()


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


class CalendarWidget(QTableView):
    def __init__(self, days, data, parent=None):
        QTableView.__init__(self, parent)
        self.setModel(CalendarModel(days, data))
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)

    def setFormData(self, department_list):
        self.setItemDelegate(FormDelegate(department_list))

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


class FormDelegate(QStyledItemDelegate):
    def __init__(self, department_list):
        QStyledItemDelegate.__init__(self)
        self.department_list = department_list

    def createEditor(self, parent, option, index):
        return ChoiceWidget(self.department_list, parent)


    # def paint(self, painter, option, index):
    #     if self.form_pixmap is not None:
    #         painter.drawPixmap(option.rect, self.form_pixmap)
    #         QStyledItemDelegate.paint(self, painter, option, index)
    #     QStyledItemDelegate.paint(self, painter, option, index)


class ChoiceWidget(QWidget):
    def __init__(self, department_list, parent):
        QWidget.__init__(self, parent)
        self.autoFillBackground()
        self.setFocusPolicy(Qt.StrongFocus)
        self.__setUi()

        self.pb_plus.clicked.connect(self.__onPlus)
        self.pb_minus.clicked.connect(self.__onMinus)
        self.pb_edit.clicked.connect(self.__onEdit)
        self.pb_cancel.clicked.connect(self.__onCancel)

        self.form = FormWidget(department_list)

    def setPersistentInfo(self):
        b = QPushButton('HAHA')
        self.l = QVBoxLayout()
        self.l.addWidget(b)
        print('hahahhaha')

    def __setUi(self):
        l = QGridLayout()
        self.pb_plus = ExpandingButton(':/img/plus.png')
        self.pb_minus = ExpandingButton(':/img/minus.png')
        self.pb_edit = ExpandingButton(':/img/edit.png')
        self.pb_cancel = ExpandingButton(':/img/cancel.png')
        l.addWidget(self.pb_plus, 0, 0)
        l.addWidget(self.pb_minus, 0, 1)
        l.addWidget(self.pb_edit, 1, 0)
        l.addWidget(self.pb_cancel, 1, 1)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(0)
        self.l = l
        self.setLayout(l)

    def __onPlus(self):
        self.form.show()

    def __onMinus(self):
        print(-1)

    def __onEdit(self):
        print(1)

    def __onCancel(self):
        self.close()


class ExpandingButton(QPushButton):
    def __init__(self, icon_path=None, parent=None):
        QPushButton.__init__(self, parent)
        if icon_path is not None:
            self.setIcon(QIcon(icon_path))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

# TODO: проверка на корректность
# TODO: Cancel & OK naming
class FormWidget(QWidget):
    hid = pyqtSignal()

    def __init__(self, department_list, parent=None):
        QWidget.__init__(self, parent)

        self.__setUi()
        self.__dataInit(department_list)

        self.res = None
        self.rb_workers.clicked.connect(self.lw_workers.show)
        self.rb_department.clicked.connect(self.__onDeprtment)
        self.rb_head.clicked.connect(self.__onHead)
        self.rb_workers.clicked.connect(self.__onWorkers)

        self.bb_dialog.helpRequested.connect(self.__onPreview)
        self.bb_dialog.accepted.connect(self.__saveResults)
        self.bb_dialog.rejected.connect(self.close)

    def __saveResults(self):
        pass

    def __dataInit(self, new_dep_list):
        self.cb_department.setModel(DepartmentModel(new_dep_list))
        self.lw_workers.setModel(WorkersModel(new_dep_list))
        self.lw_workers.setFitSize()
        self.__setDefaultState()

    def __onPreview(self):
        self.setFixedSize(self.sizeHint())
        if self.gb_secInfo.isHidden():
            self.gb_secInfo.show()
            self.pb_preview.setText('Предварительный просмотр')
        else:
            self.gb_secInfo.hide()
            self.pb_preview.setText('Вернуться к редактированию')

        self.le_name.setDisabled(self.gb_secInfo.isHidden())
        self.te_description.setDisabled(self.gb_secInfo.isHidden())
        self.cb_place.setDisabled(self.gb_secInfo.isHidden())

    def mousePressEvent(self, event):
        self.origin = event.pos()
        QDialog.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(self.pos() + (event.pos() - self.origin))

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
        self.makeYellow()

    def __onHead(self):
        self.cb_department.setEnabled(False)
        self.lw_workers.hide()
        self.makeRed()

    def __onWorkers(self):
        self.cb_department.setEnabled(False)
        self.lw_workers.show()
        self.makeGreen()

    def showDescription(self):
        self.gb_secInfo.show()

    def makeGreen(self):
        self.setStyleSheet("background-color:#c3e1ba;")

    def makeRed(self):
        self.setStyleSheet("background-color:#ee5859;")

    def makeYellow(self):
        self.setStyleSheet("background-color:#fff67a;")

    def __setUi(self):
        # Название
        le_name = QLineEdit()
        le_name.setPlaceholderText('Введите название')

        # Описание
        te_description = QTextEdit()
        te_description.setPlaceholderText("Введите описание мероприятия")

        # Место
        cb_place = QComboBox()
        cb_place.addItems(['Конференц-зал', 'Помещение отдела', 'Столовая'])

        # Длительность
        fl_duration = QFormLayout()
        sb_duration = QSpinBox()
        sb_duration.setRange(1, 8)
        fl_duration.addRow('Длительность (в ч.):', sb_duration)

        # Скрывающаяся часть
        vl_secInfo = QVBoxLayout()

        gb_participants = QGroupBox()
        gb_participants.setTitle('Участники')
        fl_participants = QFormLayout()
        cb_department = QComboBox()
        rb_department = QRadioButton('Отдел')
        rb_head = QRadioButton('Руководство')
        rb_workers = QRadioButton('Выбрать сотрудников')
        lw_workers = InfoTableView(None)
        fl_participants.addRow(rb_department, cb_department)
        fl_participants.addRow(rb_head)
        fl_participants.addRow(rb_workers)
        fl_participants.addRow(lw_workers)
        gb_participants.setLayout(fl_participants)

        vl_secInfo.addLayout(fl_duration)
        vl_secInfo.addWidget(gb_participants)

        gb_secInfo = QGroupBox()
        gb_secInfo.setLayout(vl_secInfo)

        layout = QVBoxLayout()
        layout.addWidget(le_name)
        layout.addWidget(te_description)
        layout.addWidget(cb_place)
        layout.addWidget(gb_secInfo)

        self.bb_dialog = QDialogButtonBox()
        self.pb_preview = QPushButton('Предварительный просмотр')
        self.bb_dialog.addButton(QPushButton('Отмена'), QDialogButtonBox.RejectRole)
        self.bb_dialog.addButton(QPushButton('Принять'), QDialogButtonBox.AcceptRole)
        self.bb_dialog.addButton(self.pb_preview, QDialogButtonBox.HelpRole)
        layout.addWidget(self.bb_dialog)

        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setMaximumWidth(100)

        self.le_name = le_name
        self.cb_place = cb_place
        self.vl_secInfo = vl_secInfo
        self.gb_secInfo = gb_secInfo
        self.sb_duration = sb_duration
        self.cb_department = cb_department
        self.rb_department = rb_department
        self.rb_head = rb_head
        self.rb_workers = rb_workers
        self.lw_workers = lw_workers
        self.te_description = te_description
        self.setLayout(layout)
