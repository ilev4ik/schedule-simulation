from sys import argv
from PyQt5.QtWidgets import QApplication, QTableView
from lib.models import FormDialog, ChoiceWidget
from lib.windows import MainWindow

import resources

if __name__ == '__main__':
    app = QApplication(argv)
    h = MainWindow()
    h.showMaximized()
    app.exec()