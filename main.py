from sys import argv

from PyQt5.QtWidgets import QApplication
from lib.windows import MainWindow
from PyQt5.QtCore import *

import resources

if __name__ == '__main__':
    app = QApplication(argv)
    w = MainWindow()

    w.show()
    app.exec()