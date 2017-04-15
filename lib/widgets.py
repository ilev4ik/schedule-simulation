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
from .models import DepartmentModel, CalendarModel

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




class FormDelegate(QStyledItemDelegate):
    def __init__(self):
        self.form_pixmap = None
        QStyledItemDelegate.__init__(self)

    def createEditor(self, parent, option, index):
        return ChoiceWidget(parent)

    def paint(self, painter, option, index):
        if self.form_pixmap is not None:
            painter.drawPixmap(option.rect, self.form_pixmap)
            QStyledItemDelegate.paint(self, painter, option, index)
        QStyledItemDelegate.paint(self, painter, option, index)

    def setModelData(self, editor, model, index):
        self.form_pixmap = editor.his_pixmap


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


class ChoiceWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.__setUi()

        self.pb_plus.clicked.connect(self.__onPlus)
        self.pb_minus.clicked.connect(self.__onCancel)
        self.pb_edit.clicked.connect(self.__onCancel)
        self.pb_cancel.clicked.connect(self.__onCancel)

        self.w = FormDialog()

        self.w.hid.connect(self.__onHidden)


    def __onHidden(self):
        self.his_pixmap = self.w.my_pixmap


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
        self.setLayout(l)

    def __onPlus(self):
        self.w.show()

    def __onMinus(self):
        print(-1)

    def __onEdit(self):
        print(1)

    def __onCancel(self):
        self.close()


class ExpandingButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        QPushButton.__init__(self, parent)
        self.setIcon(QIcon(icon_path))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

# TODO: проверка на корректность
class FormDialog(QWidget):
    hid = pyqtSignal()
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__setUi()
        self.__setDefaultState()
        self.rb_workers.clicked.connect(self.lw_workers.show)
        self.rb_department.clicked.connect(self.__onDeprtment)
        self.rb_head.clicked.connect(self.__onHead)
        self.rb_workers.clicked.connect(self.__onWorkers)

        self.bb_dialog.accepted.connect(self.__minimizeForm)
        self.bb_dialog.rejected.connect(self.close)

    def __minimizeForm(self):
        self.gb_secInfo.hide()
        self.setFixedSize(self.sizeHint())
        self.my_pixmap = self.getPixMap()
        self.hide()
        self.hid.emit()

    def getPixMap(self):
        return self.grab(QRect(QPoint(0, 0), self.size()))

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

    def __setUi(self):
        le_name = QTextEdit()
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

        self.bb_dialog = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        vl_secInfo.addWidget(self.bb_dialog)
        gb_secInfo = QGroupBox()

        gb_secInfo.setLayout(vl_secInfo)
        self.gb_secInfo = gb_secInfo
        layout = QVBoxLayout()
        layout.addWidget(le_name)
        layout.addWidget(cb_place)
        layout.addWidget(gb_secInfo)

        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setMaximumWidth(100)

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
