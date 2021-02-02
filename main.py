import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class CoffeeWidget(QWidget):
    def __init__(self):
        super(CoffeeWidget, self).__init__()
        uic.loadUi('main.ui', self)
        self.database_connection = sqlite3.connect('coffee.sqlite')
        self.get_data()

    def get_data(self):
        cursor = self.database_connection.cursor()
        query = 'SELECT * FROM coffee'
        result = cursor.execute(query).fetchall()
        if result:
            self.update_table(result, ['ID', 'Сорт', 'Степень обжарки', 'Вид',
                                       'Состояние', 'Описание вкуса', 'Цена',
                                       'Объем упаковки'])

    def update_table(self, data, headers=None):
        self.table.setColumnCount(len(data[0]))
        if headers is not None:
            self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)
        for i, row in enumerate(data):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, value in enumerate(data[i]):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeWidget()
    ex.show()
    sys.exit(app.exec())
