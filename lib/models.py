from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel, QAbstractListModel, QModelIndex, QVariant

from .entities import Department, Employee


class WorkersModel(QAbstractTableModel):
    def __init__(self, checked_departments: [Department]):
        QAbstractTableModel.__init__(self)
        self.data_list = []
        for dep in checked_departments:
            self.data_list.extend([[empl.getFullName(), dep.getName(), Qt.Checked] for empl in dep.getEmployeeList()])

    def getCheckedWorkers(self):
        worker_ret_list = []
        for checkable_worker in self.data_list:
            empl = Employee(checkable_worker[0], checkable_worker[1])
            state = checkable_worker[2]
            if state == Qt.Checked:
                worker_ret_list.append(empl)

        return worker_ret_list

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

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.data_list[index.row()][0]
            elif index.column() == 1:
                return self.data_list[index.row()][1]
        elif role == Qt.CheckStateRole:
            if index.column() == 0:
                return self.data_list[index.row()][2]

        return QVariant()

    def setData(self, index=QModelIndex(), value=QVariant(), role=None):
        if not index.isValid() or role != Qt.CheckStateRole:
            return False

        if role == Qt.CheckStateRole:
            self.__switchState(index.row())
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

    def __switchState(self, row):
        row_obj = self.data_list[row]
        states = [Qt.Checked, Qt.Unchecked]
        states.remove(row_obj[2])
        row_obj[2] = states[0]


class DepartmentModel(QAbstractListModel):
    def __init__(self, department_list: [Department], check_state=Qt.Unchecked):
        QAbstractListModel.__init__(self)
        self.department_list = [[dep, check_state] for dep in department_list]

    def __switchState(self, row):
        row_obj = self.department_list[row]
        states = [Qt.Checked, Qt.Unchecked]
        states.remove(row_obj[1])
        row_obj[1] = states[0]

    def uncheckAll(self):
        for (i, dep_item) in enumerate(self.department_list):
            if dep_item[1] == Qt.Checked:
                dep_item[1] = Qt.Unchecked

    def getCheckedDepartmentList(self):
        dep_ret_list = []
        for checkable_dep in self.department_list:
            dep = checkable_dep[0]
            state = checkable_dep[1]
            if state == Qt.Checked:
                dep_ret_list.append(dep)

        return dep_ret_list

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return

        return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.department_list)

    def data(self, index=QModelIndex(), role=None):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return self.department_list[index.row()][0].getName()
        elif role == Qt.CheckStateRole:
            return self.department_list[index.row()][1]

        return QVariant()

    def setData(self, index=QModelIndex(), value=QVariant(), role=None):
        if not index.isValid() or role != Qt.CheckStateRole:
            return False

        if role == Qt.CheckStateRole:
            self.__switchState(index.row())
            self.dataChanged.emit(index, index)
        return True

from .entities import Calendar
class CalendarModel(QAbstractTableModel):
    def __init__(self, calendar):
        QAbstractTableModel.__init__(self)
        self.calendar = calendar

    def clear_data(self):
        cols = self.calendar.period

        self.beginResetModel()
        self.calendar = Calendar([[[] for i in range(0, cols)] for j in range(0, 9)])
        self.endResetModel()

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return

        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def rowCount(self, parent=None, *args, **kwargs):
        return 9

    def columnCount(self, parent=None, *args, **kwargs):
        return self.calendar.period

    def data(self, index, role=None):
        row = index.row()
        col = index.column()

        if index.isValid():
            if role == Qt.DisplayRole:
                event_list = self.calendar.matrix[row][col]
                str = ""
                for event in event_list:
                    str += (event.getTitle() + '\n')

                return str
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignHCenter | Qt.AlignTop

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
