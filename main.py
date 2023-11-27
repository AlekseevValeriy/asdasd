import sqlite3
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow
from aecf import addEditCoffeeForm


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.read()
        self.add_b.clicked.connect(self.add_l)
        self.change_b.clicked.connect(self.change_l)

    def change_l(self):
        if self.name_l.text():
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            result = cur.execute("SELECT sort_name FROM coffees "
                                 "WHERE sort_name = ?", [self.name_l.text()]).fetchall()
            con.close()
            if result:
                self.a = addEditCoffeeForm(self.name_l.text(), 'change')
                self.a.show()
                self.a.exec_()
                self.read()
            else:
                self.statusBar().showMessage('Такого сорта нет в базе данных', 15000)
        else:
            self.statusBar().showMessage('Введите название', 15000)

    def add_l(self):
        if self.name_l.text():
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            result = cur.execute("SELECT sort_name FROM coffees").fetchall()
            con.close()
            if self.name_l.text() not in list(map(lambda a: a[0], result)):
                self.a = addEditCoffeeForm(self.name_l.text(), 'add')
                self.a.show()
                self.a.exec_()
                self.read()
            else:
                self.statusBar().showMessage('Такой сорт уже есть в базе данных', 15000)
        else:
            self.statusBar().showMessage('Введите название', 15000)
    def read(self):
        con = sqlite3.connect('data/coffee.sqlite')
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
