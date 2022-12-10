import sys
import os
import sqlite3
from location import *
from hotel import *
from PyQt5.QtWidgets import (QWidget, QApplication, QTabWidget, 
    QLabel, QVBoxLayout, QTableWidget, QPushButton, QListWidget, QHBoxLayout,
    QTableWidgetItem, QAbstractItemView, QHeaderView)
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QRect
from manager import *


class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_row = 0
        self.load_db()
        self.setupUi()
    
    def load_db(self):
        conn = sqlite3.connect('data.db')
        conn.execute('''
            create table if not exists locations(
                location_name varchar(100) not null primary key 
            );''')
        conn.execute('''
            create table if not exists managers (
                manager_name varchar(50) not null primary key,
                phone varchar(20),
                email varchar(30)
            );''')
        conn.execute('''
            create table if not exists hotels(
                hotel_name varchar(200) not null,
                location_name varchar(100) not null,
                manager_name varchar(50) not null,
                contact_phone varchar(20),
                description varchar(500)
            )
        ''')
        conn.commit()

        self.conn = conn

    def fill_table(self, table, table_name):
        rows = self.conn.execute(f'select * from {table_name}').fetchall()
        table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(v))

    def resize_cols(self, table, cols):
        for i, c in enumerate(cols):
            table.setColumnWidth(i, 9 * len(c))
            
    def setupUi(self):
        self.setWindowTitle('Отели')
        self.setMinimumSize(500, 300)
        self.setMaximumSize(800, 600)
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 7)
        tabwidget = QTabWidget()
        layout.addWidget(tabwidget)
        
        self.tab1 = QTableWidget()
        self.tab1.setColumnCount(5)
        cols1 = ['Название', 'Местонахождение', 'ФИО менеджера',
            'Контактный телефон', 'Описание']
        self.tab1.setHorizontalHeaderLabels(cols1)
        self.resize_cols(self.tab1, cols1)
        self.fill_table(self.tab1, 'hotels')
        tabwidget.addTab(self.tab1, 'Отели')
        self.tab2 = QTableWidget()
        self.tab2.setColumnCount(3)
        cols2 = ['ФИО', 'Телефон', 'Email']
        self.tab2.setHorizontalHeaderLabels(cols2)
        self.resize_cols(self.tab2, cols2)
        self.fill_table(self.tab2, 'managers')
        tabwidget.addTab(self.tab2, 'Менеджеры')
        self.tab3 = QTableWidget()
        self.tab3.setColumnCount(1)
        self.resize_cols(self.tab3, ['Название региона'])
        self.tab3.setHorizontalHeaderLabels(['Название региона'])
        self.fill_table(self.tab3, 'locations')
        tabwidget.addTab(self.tab3, 'Регионы')

        self.tabwidget = tabwidget

        bottom = QHBoxLayout()
        newbutt = QPushButton()
        newbutt.clicked.connect(self.create)
        newbutt.setText('Создать')
        deletebutt = QPushButton()
        deletebutt.clicked.connect(self.delete)
        deletebutt.setText('Удалить')
        editbutt = QPushButton()
        editbutt.clicked.connect(self.edit)
        editbutt.setText('Редактировать')

        for butt in [newbutt, editbutt, deletebutt]:
            butt.setFixedWidth(105)
            butt.setFixedHeight(23)
            bottom.addWidget(butt)

        layout.addLayout(bottom)

        self.tab1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab1.doubleClicked.connect(self.dbclick)
        self.tab2.doubleClicked.connect(self.dbclick)
        self.tab3.doubleClicked.connect(self.dbclick)

        self.setLayout(layout)

    def create(self):
        curr = self.tabwidget.currentIndex()
        if curr == 0:
            self.openwin(HotelDialog, self.conn)
        elif curr == 1:
            self.openwin(ManagerDialog, self.conn)
        else:
            self.openwin(LocationDialog, self.conn)


    def delete(self):
        curr = self.tabwidget.currentIndex()
        tab = [self.tab1, self.tab2, self.tab3][curr]
        fr = self.get_focused_row(tab)
        if fr is None:
            return
        name = self.get_old_name(tab, fr)
        if curr == 0:
            self.conn.execute(f'delete from hotels where hotel_name="{name}"')
        elif curr == 1:
            self.conn.execute(f'delete from managers where manager_name="{name}"')
            self.conn.execute(f'update hotels set manager_name="Н/У" where manager_name="{name}"')
        elif curr == 2:
            self.conn.execute(f'delete from locations where location_name="{name}"')
            self.conn.execute(f'update hotels set location_name="Н/У" where location_name="{name}"')
        if curr != 0:
            self.fill_table(self.tab)
        self.fill_table(self.tab1, 'hotels')
        self.conn.commit()
        
    def get_focused_row(self, tab):
        si = tab.selectedItems()
        row = si[0].row()
        for i in si[1:]:
            if i.row() != row:
                return None
        return row

    def get_data_from_row(self, table, row):
        data = []
        for j in range(table.columnCount()):
            data.append(table.item(row, j).text())
        return data
    
    def edit(self):
        curr = self.tabwidget.currentIndex()
        tab = [self.tab1, self.tab2, self.tab3][curr]
        fr = self.get_focused_row(tab)
        if fr is None:
            return
        self.edit_row = fr
        data = self.get_data_from_row(tab, fr)
        interface = [HotelDialog, ManagerDialog, LocationDialog][curr]
        self.openwin(interface, self.conn, data=data)

    def dbclick(self):
        self.edit()

    def append_table(self, table, items):
        idx = table.rowCount()
        table.insertRow(idx)
        for j, v in enumerate(items):
            table.setItem(idx, j, QTableWidgetItem(v))

    def fill_row_with(self, table, row_idx, data):
        for j, v in enumerate(data):
            table.setItem(row_idx, j, QTableWidgetItem(v))

    def get_old_name(self, table, row=None):
        if row is None:
            row = self.edit_row
        return self.get_data_from_row(table, row)[0]

    def submit_manager(self, name, phone, email, edit=False):
        if not edit:
            self.conn.execute(f'''insert into managers(manager_name, phone, email) values("{name}", "{phone}", "{email}")''')
            self.append_table(self.tab2, [name, phone, email])
        else:
            old_name = self.get_old_name(self.tab2)
            self.conn.execute(f'''update managers set manager_name="{name}", phone="{phone}", email="{email}" where manager_name="{old_name}"''')
            self.fill_row_with(self.tab2, self.edit_row, [name, phone, email])
        self.conn.commit()
    
    def submit_location(self, name, edit=False):
        if not edit:
            self.conn.execute(f'insert into locations(location_name) values("{name}")')
            self.append_table(self.tab3, [name])
        else:
            old_name = self.get_old_name(self.tab3)
            self.conn.execute(f'''update locations set location_name="{name}" where location_name="{old_name}"''')
            self.fill_row_with(self.tab3, self.edit_row, [name])
        self.conn.commit()

    def submit_hotel(self, hotel_name, location_name, manager_name, contact_phone, description, edit=False):
        if not edit:
            self.conn.execute(f'''insert into hotels(hotel_name, location_name, manager_name, contact_phone, description)
                values ("{hotel_name}", "{location_name}", "{manager_name}", "{contact_phone}", "{description}")''')
            self.append_table(self.tab1, [hotel_name, location_name, manager_name, contact_phone, description])
        else:
            old_name = self.get_old_name(self.tab1)
            self.conn.execute(f'''update hotels set hotel_name="{hotel_name}", location_name="{location_name}", manager_name="{manager_name}",
                contact_phone="{contact_phone}", description="{description}" where hotel_name="{old_name}"''')
            self.fill_row_with(self.tab1, self.edit_row, [hotel_name, location_name, manager_name, contact_phone, description])
        self.conn.commit()

    def openwin(self, t, *args, **kwargs):
        self.sub = QtWidgets.QMainWindow()
        self.sub_ui = t(self, *args, **kwargs)
        self.sub_ui.setupUi(self.sub)
        self.sub.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())