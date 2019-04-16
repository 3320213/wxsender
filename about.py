# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgAbout(object):
    def setupUi(self, dlgAbout):
        dlgAbout.setObjectName("dlgAbout")
        dlgAbout.resize(246, 86)
        dlgAbout.setAcceptDrops(False)
        dlgAbout.setSizeGripEnabled(False)
        dlgAbout.setModal(False)
        self.label = QtWidgets.QLabel(dlgAbout)
        self.label.setGeometry(QtCore.QRect(179, 60, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dlgAbout)
        self.label_2.setGeometry(QtCore.QRect(50, 26, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(dlgAbout)
        QtCore.QMetaObject.connectSlotsByName(dlgAbout)

    def retranslateUi(self, dlgAbout):
        _translate = QtCore.QCoreApplication.translate
        dlgAbout.setWindowTitle(_translate("dlgAbout", "关于软件"))
        self.label.setText(_translate("dlgAbout", "for luobo"))
        self.label_2.setText(_translate("dlgAbout", "微信群发助手"))

