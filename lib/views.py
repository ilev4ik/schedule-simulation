from PyQt5.Qt import *
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView, QListView

from .tools import getTableContentFitWidth
from .models import WorkersModel, DepartmentModel


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
