import sys
import os
import sqlite3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem

CREATE_DATABASE_SCRIPT = """CREATE TABLE coffee (
    id             INTEGER      PRIMARY KEY AUTOINCREMENT
                                UNIQUE
                                NOT NULL,
    name           STRING (255),
    bake_grade     STRING (255),
    state          STRING (255),
    taste_describe TEXT (1024),
    price          INTEGER,
    package_volume INTEGER
);
"""


class CoffeeWidgetUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(629, 469)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_add = QtWidgets.QPushButton(Form)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.btn_edit = QtWidgets.QPushButton(Form)
        self.btn_edit.setObjectName("btn_edit")
        self.horizontalLayout.addWidget(self.btn_edit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Кофе"))
        self.btn_add.setText(_translate("Form", "Добавить запись"))
        self.btn_edit.setText(_translate("Form", "Редактировать"))


class AddEditCoffeeWindowUiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(404, 370)
        Form.setMaximumSize(QtCore.QSize(16777215, 370))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.edit_name = QtWidgets.QLineEdit(Form)
        self.edit_name.setObjectName("edit_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.edit_name)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.edit_bake_grade = QtWidgets.QLineEdit(Form)
        self.edit_bake_grade.setObjectName("edit_bake_grade")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.edit_bake_grade)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.edit_state = QtWidgets.QLineEdit(Form)
        self.edit_state.setObjectName("edit_state")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.edit_state)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.edit_price = QtWidgets.QLineEdit(Form)
        self.edit_price.setObjectName("edit_price")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.edit_price)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.edit_package_volume = QtWidgets.QLineEdit(Form)
        self.edit_package_volume.setObjectName("edit_package_volume")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.edit_package_volume)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.edit_describe = QtWidgets.QTextEdit(Form)
        self.edit_describe.setObjectName("edit_describe")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.edit_describe)
        self.verticalLayout.addLayout(self.formLayout)
        self.btn_done = QtWidgets.QPushButton(Form)
        self.btn_done.setObjectName("btn_done")
        self.verticalLayout.addWidget(self.btn_done)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактирование записи"))
        self.label.setText(_translate("Form", "Название кофе"))
        self.label_2.setText(_translate("Form", "Степень обжарки"))
        self.label_3.setText(_translate("Form", "Молотый/зерновой"))
        self.label_5.setText(_translate("Form", "Цена"))
        self.label_6.setText(_translate("Form", "Объем упаковки"))
        self.label_4.setText(_translate("Form", "Описание вкуса"))
        self.btn_done.setText(_translate("Form", "Сохранить"))


class AddEditCoffeeWindow(AddEditCoffeeWindowUiForm, QWidget):
    def __init__(self, parent_window, change=None):
        super(AddEditCoffeeWindow, self).__init__()
        self.setupUi(self)
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


class CoffeeWidget(CoffeeWidgetUiForm, QWidget):
    def __init__(self):
        super(CoffeeWidget, self).__init__()
        self.setupUi(self)

        self.child_window = None

        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_edit.clicked.connect(self.btn_edit_clicked)

        for _, dirs, _ in os.walk(os.getcwd()):
            if 'data' not in dirs:
                os.mkdir('data')
            break

        self.database_connection = sqlite3.connect('data\\coffee.sqlite')

        try:
            self.database_connection.cursor().execute('SELECT * FROM coffee').fetchall()
        except Exception:
            self.database_connection.cursor().execute(CREATE_DATABASE_SCRIPT)

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
