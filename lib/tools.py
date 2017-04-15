
def getTableContentFitWidth(t, c):
    w = t.verticalHeader().width() + 18 # magic constant
    for i in range(0, c, 1):
        w += t.columnWidth(i)
    return w