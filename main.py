import sqlite3
import sys

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from aecf import addEditCoffeeForm


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.read()
        self.add_b.clicked.connect(self.add_l)

    def add_l(self):
        self.a = addEditCoffeeForm()
        self.a.show()
        self.a.exec_()
        self.read()

    def read(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("SELECT * FROM coffees").fetchall()

        con.close()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        for n, i in enumerate(result):
            for j in range(7):
                self.tableWidget.setItem(n, j, QtWidgets.QTableWidgetItem(str(i[j])))


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec())
