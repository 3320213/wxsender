# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wxlogin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgLogin(object):
    def setupUi(self, dlgLogin):
        dlgLogin.setObjectName("dlgLogin")
        dlgLogin.resize(400, 300)

        self.retranslateUi(dlgLogin)
        QtCore.QMetaObject.connectSlotsByName(dlgLogin)

    def retranslateUi(self, dlgLogin):
        _translate = QtCore.QCoreApplication.translate
        dlgLogin.setWindowTitle(_translate("dlgLogin", "请扫描二维码登录"))

