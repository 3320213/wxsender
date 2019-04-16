# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DlgSender(object):
    def setupUi(self, DlgSender):
        DlgSender.setObjectName("DlgSender")
        DlgSender.resize(448, 532)
        self.btSave = QtWidgets.QPushButton(DlgSender)
        self.btSave.setGeometry(QtCore.QRect(360, 483, 75, 26))
        self.btSave.setObjectName("btSave")
        self.groupBox = QtWidgets.QGroupBox(DlgSender)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 441, 381))
        self.groupBox.setObjectName("groupBox")
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox)
        self.treeWidget.setGeometry(QtCore.QRect(10, 22, 421, 351))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.txtWorkdir = QtWidgets.QTextEdit(DlgSender)
        self.txtWorkdir.setGeometry(QtCore.QRect(90, 400, 261, 26))
        self.txtWorkdir.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtWorkdir.setObjectName("txtWorkdir")
        self.btBrowser = QtWidgets.QPushButton(DlgSender)
        self.btBrowser.setGeometry(QtCore.QRect(360, 400, 75, 26))
        self.btBrowser.setObjectName("btBrowser")
        self.label = QtWidgets.QLabel(DlgSender)
        self.label.setGeometry(QtCore.QRect(10, 402, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(DlgSender)
        self.label_2.setGeometry(QtCore.QRect(10, 430, 401, 16))
        self.label_2.setObjectName("label_2")
        self.txtSndLag = QtWidgets.QTextEdit(DlgSender)
        self.txtSndLag.setGeometry(QtCore.QRect(90, 450, 61, 26))
        self.txtSndLag.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.txtSndLag.setObjectName("txtSndLag")
        self.label_3 = QtWidgets.QLabel(DlgSender)
        self.label_3.setGeometry(QtCore.QRect(10, 452, 71, 21))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(DlgSender)
        self.label_5.setGeometry(QtCore.QRect(10, 485, 71, 21))
        self.label_5.setObjectName("label_5")
        self.txtSndCnt = QtWidgets.QTextEdit(DlgSender)
        self.txtSndCnt.setGeometry(QtCore.QRect(90, 485, 61, 26))
        self.txtSndCnt.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.txtSndCnt.setObjectName("txtSndCnt")
        self.label_6 = QtWidgets.QLabel(DlgSender)
        self.label_6.setGeometry(QtCore.QRect(370, 456, 61, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(DlgSender)
        self.label_7.setGeometry(QtCore.QRect(165, 452, 141, 21))
        self.label_7.setObjectName("label_7")
        self.txtSndLagT = QtWidgets.QTextEdit(DlgSender)
        self.txtSndLagT.setGeometry(QtCore.QRect(303, 450, 61, 26))
        self.txtSndLagT.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.txtSndLagT.setObjectName("txtSndLagT")
        self.label_8 = QtWidgets.QLabel(DlgSender)
        self.label_8.setGeometry(QtCore.QRect(162, 485, 111, 21))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(DlgSender)
        QtCore.QMetaObject.connectSlotsByName(DlgSender)

    def retranslateUi(self, DlgSender):
        _translate = QtCore.QCoreApplication.translate
        DlgSender.setWindowTitle(_translate("DlgSender", "发送设置"))
        self.btSave.setText(_translate("DlgSender", "保存配置"))
        self.groupBox.setTitle(_translate("DlgSender", "勾选产品信息发送的微信群"))
        self.btBrowser.setText(_translate("DlgSender", "选择目录"))
        self.label.setText(_translate("DlgSender", "设置工作目录"))
        self.label_2.setText(_translate("DlgSender", "工作目录下每个产品一个目录,产品目录下存放要发送的图片和消息"))
        self.label_3.setText(_translate("DlgSender", "发送间隔(秒)"))
        self.label_5.setText(_translate("DlgSender", "循环发送次数"))
        self.label_6.setText(_translate("DlgSender", "秒重复发送"))
        self.label_7.setText(_translate("DlgSender", "所有产品发送完成后等待"))
        self.label_8.setText(_translate("DlgSender", "0表示无限循环发送"))

