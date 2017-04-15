from PyQt5.Qt import *
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant

from .entities import Department, Worker


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


class CalendarModel(QAbstractTableModel):
    def __init__(self, cols):
        QAbstractTableModel.__init__(self)
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
        # if role == Qt.DisplayRole:
        #     return 'hmm'

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
