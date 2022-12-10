from PyQt5 import QtCore, QtGui, QtWidgets
from toolz import *


class HotelDialog(object):
    def __init__(self, parent, conn, data=None):
        super(HotelDialog, self).__init__()
        self.conn = conn
        self.parent = parent
        self.load_choices()
        self.data = data

    def load_choices(self):
        nnch = [('Н/У',)]
        self.available_locations = nnch + self.conn.execute('select location_name from locations').fetchall()
        self.available_managers = nnch + self.conn.execute('select manager_name from managers').fetchall()
        for arr in [self.available_locations, self.available_managers]:
            for i in range(len(arr)):
                arr[i] = arr[i][0]
    
    def submit(self):
        hotel_name = self.lineEdit.text()
        location_name = self.comboBox.currentText()
        manager_name = self.comboBox_2.currentText()
        contact_phone = self.lineEdit_2.text()
        description = self.plainTextEdit.toPlainText()

        if not strweight(hotel_name):
            return error('Необходимо указать название отеля!')
        elif not strweight(contact_phone):
            return error('Необходимо указать контактный телефон!')
        elif not self.edit and self.conn.execute(f'select * from hotels where hotel_name = "{hotel_name}"').fetchone() is not None:
            return error('Отель с таким названием уже записан!')
        
        self.parent.submit_hotel(hotel_name, location_name, manager_name, contact_phone, description, edit=self.edit)
        self.win.close()

    def prepare(self):
        if self.data is not None:
            self.edit = True
            self.lineEdit.setText(self.data[0])
            self.comboBox.setCurrentText(self.data[1])
            self.comboBox_2.setCurrentText(self.data[2])
            self.lineEdit_2.setText(self.data[3])
            self.plainTextEdit.setPlainText(self.data[4])
        else: self.edit = False

    def setupUi(self, MainWindow):
        self.win = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(406, 251)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 201))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.plainTextEdit)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(325, 220, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 220, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(MainWindow.close)
        MainWindow.setCentralWidget(self.centralwidget)
        self.comboBox.addItems(self.available_locations)
        self.comboBox_2.addItems(self.available_managers)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.prepare()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Регистрация отеля"))
        self.label.setText(_translate("MainWindow", "Имя отеля"))
        self.label_2.setText(_translate("MainWindow", "Местонахождение"))
        self.label_4.setText(_translate("MainWindow", "ФИО менеджера"))
        self.label_3.setText(_translate("MainWindow", "Контактный телефон"))
        self.label_5.setText(_translate("MainWindow", "Описание отеля"))
        self.pushButton.setText(_translate("MainWindow", "ОК"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))

