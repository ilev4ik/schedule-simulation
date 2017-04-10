from PyQt5.QtCore import QAbstractListModel, QModelIndex
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from PyQt5.QtWidgets import QListView
from PyQt5.Qt import * # enums


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


class Depatment(object):
    def __init__(self, name, s):
        object.__init__(self)
        self.name = name
        self.state = s

    def switchState(self):
        states = [Qt.Checked, Qt.Unchecked]
        states.remove(self.state)
        self.state = states[0]


class DepartmentModel(QAbstractListModel):
    def __init__(self):
        QAbstractListModel.__init__(self)
        self.data_list = []
        QAbstractListModel.beginResetModel(self)
        self.__readData()
        QAbstractListModel.endResetModel(self)

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return
        return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self.data_list)

    def data(self, index=QModelIndex(), role=None):
        if not index.isValid():
            return QVariant()

        w = self.data_list[index.row()]
        if role == Qt.DisplayRole:
            return w.name
        elif role == Qt.CheckStateRole:
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
        count = 0
        while not stream.atEnd():
            count += 1
            line = stream.readLine()
            self.data_list.append(Depatment(line, Qt.Checked))

        if count == 0:
            raise Exception('resource ' + file_name + ' has no items')


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