from sys import argv
from PyQt5.QtWidgets import QApplication

from src.windows import MainWindow


import resources

if __name__ == '__main__':
    app = QApplication(argv)
    h = MainWindow()
    h.showMaximized()

    app.exec()