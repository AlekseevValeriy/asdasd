import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from addEditCoffeeForm import Ui_Dialog


class addEditCoffeeForm(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add)

    def add(self):
        lic = [self.l1.text(), self.l2.text(), self.l3.text(), self.l4.text(), self.l5.text(), self.l6.text()]
        try:
            if not any([n.isdigit() for n in (lic[-1], lic[-2])]):
                raise TypeError
            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()
            command = ("INSERT INTO coffees(sort_name, degree_roasting, condition, taste, price, volume) "
                       "VALUES (?, ?, ?, ?, ?, ?)")
            cur.execute(command, lic)
            con.commit()
            con.close()
            self.close()
        except sqlite3.IntegrityError:
            self.errors.setText('Такое название уже существует')
        except TypeError:
            self.errors.setText('Неверный тип данных')
        except Exception as error:
            self.errors.setText(f"{error, type(error).__name__, error.__traceback__}")


