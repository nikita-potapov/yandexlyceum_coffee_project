import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class AddEditCoffeeWindow(QWidget):
    def __init__(self, parent_window, change=None):
        super(AddEditCoffeeWindow, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parent_window = parent_window
        self.change = change
        if change is not None:
            self.fill_table()

        self.btn_done.clicked.connect(self.btn_save_clicked)

    def fill_table(self):
        cursor = self.parent_window.database_connection.cursor()
        query = f"""SELECT * FROM coffee WHERE id = {self.change}"""
        result = cursor.execute(query).fetchone()
        if result:
            coffee_id, coffee_name, bake_grade, state, \
            taste_describe, price, package_volume = result
            self.edit_name.setText(coffee_name)
            self.edit_bake_grade.setText(bake_grade)
            self.edit_state.setText(state)
            self.edit_price.setText(str(price))
            self.edit_package_volume.setText(str(package_volume))
            self.edit_describe.setText(taste_describe)

    def btn_save_clicked(self):
        name = self.edit_name.text()
        bake = self.edit_bake_grade.text()
        state = self.edit_state.text()
        price = self.edit_price.text()
        package_volume = self.edit_package_volume.text()
        describe = self.edit_describe.toPlainText()

        cursor = self.parent_window.database_connection.cursor()
        if self.change is not None:
            query = f"""UPDATE coffee SET name = '{name}', bake_grade = '{bake}',
                            state = '{state}', taste_describe = '{describe}',
                             price = {price}, package_volume = {package_volume}
                              WHERE id = {self.change}"""
        else:
            query = f"""INSERT INTO coffee(name, bake_grade, state,
             taste_describe, price, package_volume) VALUES('{name}', '{bake}', '{state}',
             '{describe}', '{price}', '{package_volume}')"""

        cursor.execute(query)
        self.parent_window.database_connection.commit()

        self.close()

    def closeEvent(self, event):
        self.parent_window.setDisabled(False)
        self.parent_window.get_data()
        self.parent_window.show()
        self.close()


class CoffeeWidget(QWidget):
    def __init__(self):
        super(CoffeeWidget, self).__init__()
        uic.loadUi('main.ui', self)

        self.child_window = None

        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_edit.clicked.connect(self.btn_edit_clicked)

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

    def btn_add_clicked(self):
        self.setDisabled(True)
        self.child_window = AddEditCoffeeWindow(self)
        self.child_window.show()

    def btn_edit_clicked(self):
        selected_row = list(self.table.selectedItems())
        if selected_row:
            selected_id = int(selected_row[0].text())
            self.setDisabled(True)
            self.child_window = AddEditCoffeeWindow(self, change=selected_id)
            self.child_window.show()

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
