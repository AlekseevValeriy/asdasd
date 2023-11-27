import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class addEditCoffeeForm(QDialog):
    def __init__(self, name, status):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.name = name
        self.l1.setText(self.name)
        if status == 'add':
            self.pushButton.clicked.connect(self.add)
        elif status == 'change':
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            result = cur.execute("SELECT degree_roasting, condition, taste, price, volume FROM coffees "
                                 "WHERE sort_name = ?", [self.name]).fetchall()
            con.close()
            self.l2.setText(result[0][0])
            self.l3.setText(result[0][1])
            self.l4.setText(result[0][2])
            self.l5.setText(str(result[0][3]))
            self.l6.setText(str(result[0][4]))
            self.pushButton.clicked.connect(self.change)

    def add(self):
        lic = [self.l1.text(), self.l2.text(), self.l3.text(), self.l4.text(), self.l5.text(), self.l6.text()]

        try:
            if not any([n.isdigit() for n in (lic[-1], lic[-2])]):
                raise TypeError
            con = sqlite3.connect('coffee.sqlite')
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

    def change(self):
        lic = [self.l1.text(), self.l2.text(), self.l3.text(), self.l4.text(), self.l5.text(), self.l6.text(),
               self.name]
        try:
            if not any([n.isdigit() for n in (lic[-1], lic[-2])]):
                raise TypeError
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            command = ("UPDATE coffees "
                       "SET sort_name = ?, degree_roasting = ?, condition = ?, taste = ?, price = ?, volume = ?"
                       "WHERE sort_name = ?")
            cur.execute(command, lic)
            con.commit()
            con.close()
            self.close()
        except TypeError:
            self.errors.setText('Неверный тип данных')
        except Exception as error:
            self.errors.setText(f"{error, type(error).__name__, error.__traceback__}")
