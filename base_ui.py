# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'base_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1031, 727)
        MainWindow.setMinimumSize(QtCore.QSize(390, 220))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.groupBox = QtWidgets.QGroupBox(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.btn_tool_1 = QtWidgets.QToolButton(self.groupBox)
        self.btn_tool_1.setObjectName("btn_tool_1")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btn_tool_1)
        self.btn_1 = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_1.sizePolicy().hasHeightForWidth())
        self.btn_1.setSizePolicy(sizePolicy)
        self.btn_1.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_1.setObjectName("btn_1")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.btn_1)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.line)
        self.lineEdit_1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lineEdit_1)
        self.verticalLayout.addWidget(self.groupBox)
        self.label_3 = QtWidgets.QLabel(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lineEdit_2)
        self.btn_tool_2 = QtWidgets.QToolButton(self.groupBox_2)
        self.btn_tool_2.setObjectName("btn_tool_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btn_tool_2)
        self.btn_4 = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_4.sizePolicy().hasHeightForWidth())
        self.btn_4.setSizePolicy(sizePolicy)
        self.btn_4.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_4.setObjectName("btn_4")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.btn_4)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.table_1 = QtWidgets.QTableView(self.tab_1)
        self.table_1.setObjectName("table_1")
        self.horizontalLayout.addWidget(self.table_1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.btn_3 = QtWidgets.QPushButton(self.tab_3)
        self.btn_3.setGeometry(QtCore.QRect(150, 90, 108, 32))
        self.btn_3.setObjectName("btn_3")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_3)
        self.graphicsView.setGeometry(QtCore.QRect(30, 180, 771, 221))
        self.graphicsView.setObjectName("graphicsView")
        self.lcdNumber = QtWidgets.QLCDNumber(self.tab_3)
        self.lcdNumber.setGeometry(QtCore.QRect(69, 480, 121, 61))
        self.lcdNumber.setObjectName("lcdNumber")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(60, 460, 151, 16))
        self.label.setObjectName("label")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.tab_3)
        self.lcdNumber_2.setGeometry(QtCore.QRect(70, 570, 121, 61))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(110, 550, 31, 16))
        self.label_4.setObjectName("label_4")
        self.listWidget = QtWidgets.QListWidget(self.tab_3)
        self.listWidget.setGeometry(QtCore.QRect(520, 60, 231, 21))
        self.listWidget.setObjectName("listWidget")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(520, 30, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(350, 30, 111, 16))
        self.label_6.setObjectName("label_6")
        self.radioButton = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton.setGeometry(QtCore.QRect(350, 54, 100, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_2.setGeometry(QtCore.QRect(350, 74, 100, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_3.setGeometry(QtCore.QRect(350, 94, 100, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(50, 30, 111, 16))
        self.label_7.setObjectName("label_7")
        self.textEdit = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit.setGeometry(QtCore.QRect(50, 60, 201, 21))
        self.textEdit.setObjectName("textEdit")
        self.toolButton = QtWidgets.QToolButton(self.tab_3)
        self.toolButton.setGeometry(QtCore.QRect(260, 59, 26, 22))
        self.toolButton.setObjectName("toolButton")
        self.btn_6 = QtWidgets.QPushButton(self.tab_3)
        self.btn_6.setGeometry(QtCore.QRect(43, 90, 108, 32))
        self.btn_6.setObjectName("btn_6")
        self.listWidget_2 = QtWidgets.QListWidget(self.tab_3)
        self.listWidget_2.setGeometry(QtCore.QRect(150, 150, 271, 21))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(40, 150, 111, 16))
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(300, 430, 81, 16))
        self.label_10.setObjectName("label_10")
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.tab_3)
        self.lcdNumber_3.setGeometry(QtCore.QRect(280, 480, 121, 61))
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.tab_3)
        self.lcdNumber_4.setGeometry(QtCore.QRect(282, 570, 121, 61))
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.label_11 = QtWidgets.QLabel(self.tab_3)
        self.label_11.setGeometry(QtCore.QRect(74, 430, 111, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_3)
        self.label_12.setGeometry(QtCore.QRect(300, 460, 81, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab_3)
        self.label_13.setGeometry(QtCore.QRect(280, 550, 131, 16))
        self.label_13.setObjectName("label_13")
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Портфель ИТ и ЦТ"))
        self.label_2.setText(_translate("MainWindow", "Extraction"))
        self.groupBox.setTitle(_translate("MainWindow", "Choose file"))
        self.btn_tool_1.setText(_translate("MainWindow", "..."))
        self.btn_1.setText(_translate("MainWindow", "Extract FEM"))
        self.label_3.setText(_translate("MainWindow", "Mapping"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Choose mapping file"))
        self.btn_tool_2.setText(_translate("MainWindow", "..."))
        self.btn_4.setText(_translate("MainWindow", "Apply Map"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Extraction"))
        self.btn_3.setText(_translate("MainWindow", "calculation"))
        self.label.setText(_translate("MainWindow", "EMV (NPV, UMV, DMV)"))
        self.label_4.setText(_translate("MainWindow", "J (PI)"))
        self.label_5.setText(_translate("MainWindow", "Choose item"))
        self.label_6.setText(_translate("MainWindow", "Choose granula"))
        self.radioButton.setText(_translate("MainWindow", "Portfel"))
        self.radioButton_2.setText(_translate("MainWindow", "Programme"))
        self.radioButton_3.setText(_translate("MainWindow", "Project"))
        self.label_7.setText(_translate("MainWindow", "Choose file"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.btn_6.setText(_translate("MainWindow", "apply"))
        self.label_8.setText(_translate("MainWindow", "Choose granula"))
        self.label_10.setText(_translate("MainWindow", "Ковенанты"))
        self.label_11.setText(_translate("MainWindow", "Эффективность"))
        self.label_12.setText(_translate("MainWindow", "capex / opex"))
        self.label_13.setText(_translate("MainWindow", "Inv (NPV) / Inv (DMV)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Calc"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
