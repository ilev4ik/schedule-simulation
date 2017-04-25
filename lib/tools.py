def getTableContentFitWidth(t, c):
    w = t.verticalHeader().width() + t.verticalScrollBar().sizeHint().width()
    for i in range(0, c, 1):
        w += t.columnWidth(i)
    return w

from PyQt5.QtCore import QThread
class Sleeper(QThread):
    def __init__(self, func):
        QThread.__init__(self)
        self.func = func

    def run(self):
        self.func()
