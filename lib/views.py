from PyQt5.Qt import *
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView, QListView

from .tools import getTableContentFitWidth
from .models import WorkersModel, DepartmentModel

class InfoTableView(QTableView):
    def __init__(self, model=None):
        QTableView.__init__(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        if model is not None:
            self.setModel(model)
            self.setFitSize()

    def setFitSize(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setFixedWidth(getTableContentFitWidth(self, self.model().columnCount()))


class InfoListView(QListView):
    def __init__(self, model):
        QListView.__init__(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setModel(model)
