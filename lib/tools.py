def getTableContentFitWidth(t, c):
    w = t.verticalHeader().width() + t.verticalScrollBar().sizeHint().width()
    for i in range(0, c, 1):
        w += t.columnWidth(i)
    return w