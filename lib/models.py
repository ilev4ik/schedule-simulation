from PyQt5.Qt import * # enums


# TODO: проверка на корректность
class FormDialog(QDialog):
    def __init__(self, nextParent=None, parent=None):
        self.nextParent = nextParent
        QDialog.__init__(self, parent)
        self.__setUi()
        self.__setDefaultState()
        self.rb_workers.clicked.connect(self.lw_workers.show)
        self.rb_department.clicked.connect(self.__onDeprtment)
        self.rb_head.clicked.connect(self.__onHead)
        self.rb_workers.clicked.connect(self.__onWorkers)

        self.bb_dialog.accepted.connect(self.__minimizeForm)
        self.bb_dialog.rejected.connect(self.close)
        self.makeYellow()

    def __minimizeForm(self):
        self.gb_secInfo.hide()
        self.setParent(self.nextParent)

    def __setUi(self):
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


class Worker(object):
    def __init__(self, fname, lname, dep, s):
        object.__init__(self)
        self.name = fname
        self.surname = lname
        self.department = dep
        self.state = s

    def switchState(self):
        states = [Qt.Checked, Qt.Unchecked]
        states.remove(self.state)
        self.state = states[0]

    def fullName(self):
        return self.name + ' ' + self.surname


class WorkersModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.data_list = []
        QAbstractTableModel.beginResetModel(self)
        self.__readData()
        QAbstractTableModel.endResetModel(self)

    def flags(self, index=QModelIndex()):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        elif index.column() == 1:
            return Qt.ItemIsEnabled

    def rowCount(self, parent=QModelIndex(), **kwargs):
        return len(self.data_list)

    def columnCount(self, QModelIndex_parent=QModelIndex(), *args, **kwargs):
        return 2

    def data(self, index=QModelIndex(), role=None):
        if not index.isValid():
            return QVariant()

        w = self.data_list[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return w.fullName()
            elif index.column() == 1:
                return w.department
        elif role == Qt.CheckStateRole:
            if index.column() == 0:
                return w.state

        return QVariant()

    def setData(self, index=QModelIndex(), value=QVariant(), role=None):
        if not index.isValid() or role != Qt.CheckStateRole:
            return False
        self.data_list[index.row()].switchState()
        self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role=None):
        header = ['Сотрудники', 'Департамент']
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return header[section]
            elif orientation == Qt.Vertical:
                return range(1, len(self.data_list) + 1)[section]

        return QVariant()

    def __readData(self):
        file_list = [
            'analytics','bookkeeping','development',
            'finances','hr','marketing','purchasing',
            'sales','testing'
            ]
        path = ':/stuff/'
        for file_name in file_list:
            count = 0
            file = QFile(path + file_name + '.txt')
            if not file.open(QIODevice.ReadOnly | QIODevice.Text):
                raise Exception('resource ' + file_name + ' error while openning')

            stream = QTextStream(file)
            stream.setCodec('UTF-8')
            dep_name = stream.readLine()
            if dep_name[-1] != ':':
                raise Exception('resource ' + file_name + ' with no department mark')

            while not stream.atEnd():
                count += 1
                line = stream.readLine()

                (n, s) = line.split()

                self.data_list.append(Worker(n, s, dep_name[:-1], Qt.Unchecked))

            if count == 0:
                raise Exception('resource ' + file_name + ' has no items')


class Department(object):
    def __init__(self, name, s):
        object.__init__(self)
        self.name = name
        self.state = s

    def switchState(self):
        states = [Qt.Checked, Qt.Unchecked]
        states.remove(self.state)
        self.state = states[0]


class DepartmentModel(QAbstractListModel):
    def __init__(self, checkable=True):
        QAbstractListModel.__init__(self)
        self.data_list = []
        self.checkable = checkable
        QAbstractListModel.beginResetModel(self)
        self.__readData()
        QAbstractListModel.endResetModel(self)

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return
        f = Qt.ItemIsEnabled
        return  f | Qt.ItemIsUserCheckable if self.checkable else f | Qt.ItemIsSelectable

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self.data_list)

    def data(self, index=QModelIndex(), role=None):
        if not index.isValid():
            return QVariant()

        w = self.data_list[index.row()]
        if role == Qt.DisplayRole:
            return w.name
        elif role == Qt.CheckStateRole and self.checkable:
            return w.state

        return QVariant()

    def setData(self, index=QModelIndex(), value=QVariant(), role=None):
        if not index.isValid() or role != Qt.CheckStateRole:
            return False
        self.data_list[index.row()].switchState()
        self.dataChanged.emit(index, index)
        return True

    def __readData(self):
        file_name = 'departments'
        path = ':/office/'
        file = QFile(path + file_name + '.txt')

        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            raise Exception('resource ' + file_name + ' error while openning')

        stream = QTextStream(file)
        stream.setCodec("UTF-8")
        count = 0
        while not stream.atEnd():
            count += 1
            line = stream.readLine()
            self.data_list.append(Department(line, Qt.Checked))

        if count == 0:
            raise Exception('resource ' + file_name + ' has no items')


class ExpandingButton(QPushButton):
    def __init__(self, icon_path, parent=None):
        QPushButton.__init__(self, parent)
        self.setIcon(QIcon(icon_path))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class ChoiceWidget(QWidget):
    def __init__(self, parent=None):
        self.nextParent = parent
        QWidget.__init__(self, parent)
        self.__setUi(parent)

        self.pb_plus.clicked.connect(self.__onPlus)
        self.pb_minus.clicked.connect(self.__onCancel)
        self.pb_edit.clicked.connect(self.__onCancel)
        self.pb_cancel.clicked.connect(self.__onCancel)

    def __setUi(self, parent):
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
        w = FormDialog(self.nextParent, self)
        w.show()

    def __onMinus(self):
        print(-1)

    def __onEdit(self):
        print(1)

    def __onCancel(self):
        self.close()


class FormDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)

    def createEditor(self, parent, option, index):
        return ChoiceWidget(parent)


class CalendarModel(QAbstractTableModel):
    def __init__(self, cols):
        QAbstractTableModel.__init__(self)
        self.data_matrix = FormDialog()
        self.col_num = cols

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return

        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def rowCount(self, parent=None, *args, **kwargs):
        return 9

    def columnCount(self, parent=None, *args, **kwargs):
        return self.col_num

    def data(self, QModelIndex, role=None):
        if role == Qt.DisplayRole:
            return 'hmm'

        return QVariant()

    def headerData(self, section, orientation, role=None):
        hor_header = ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                      'Пятница', 'Суббота', 'Воскресенье']
        ver_header = ['10:00','11:00','12:00','13:00','14:00',
                      '15:00','16:00','17:00','18:00']

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return hor_header[section % 7] + '\nДень ' + str(section + 1)
            elif orientation == Qt.Vertical and section < 9:
                return ver_header[section]
        return QVariant()

    def setData(self, index=QModelIndex(), value=QVariant(), role=None):
        if not index.isValid() or role != Qt.CheckStateRole:
            return False

        if role == Qt.EditRole:
            return
        return True




def getTableContentFitWidth(t, c):
    w = t.verticalHeader().width() + 18 # magic constant
    for i in range(0, c, 1):
        w += t.columnWidth(i)
    return w


class InfoTableView(QTableView):
    def __init__(self):
        QTableView.__init__(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setModel(WorkersModel())
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setFixedWidth(getTableContentFitWidth(self, self.model().columnCount()))


class InfoListView(QListView):
    def __init__(self):
        QListView.__init__(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setModel(DepartmentModel())

