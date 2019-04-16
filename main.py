# -*- coding: utf-8 -*-
import sys
import os

import setting
import about
import wxlogin
import threading
from utils import Utils

#from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from wxsender import wxsender
wxsnd = wxsender()


class WxLoginGUI(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = wxlogin.Ui_dlgLogin()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.ui.setupUi(self)

        self.isLogin = False
        self.layout = QVBoxLayout()
        self.lab1 = QLabel()
        #self.show()
        self.initUI()

    def initUI(self):
        bytePic = wxsnd.get_login_qrcode_pic()
        image = QImage.fromData(bytePic)

        self.pixmap = QPixmap.fromImage(image)
        #self.png = QPixmap.loadFromData()wxsnd
        self.showQrcodePic()
        self.tlogin = threading.Thread(target=self.thread_wait_for_login)
        self.tlogin.start()

    def showQrcodePic(self):

        self.lab1.setPixmap(self.pixmap)
        self.layout.addWidget(self.lab1)
        self.setLayout(self.layout)


    def thread_wait_for_login(self):
        ret = 1
        while ret == 1:
            ret = wxsnd.waitting_for_login()
            if ret == 0:
                self.isLogin = True
                break
            elif ret == 1:
                print("time out!!!")
                bytePic = wxsnd.get_login_qrcode_pic()
                image = QImage.fromData(bytePic)

                self.pixmap = QPixmap.fromImage(image)
                # self.png = QPixmap.loadFromData()wxsnd
                self.showQrcodePic()
            else:
                print("man closed!!!")
                break
        self.close()


    def closeEvent(self, event):
        wxsnd.isStop = True
        #self.tlogin.join(2)
        #Utils.stop_thread(self.tlogin)
        event.accept()

class AboutGUI(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui1 = about.Ui_dlgAbout()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.ui1.setupUi(self)
        self.show()


class SetGUI(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = setting.Ui_DlgSender()
        self.save_conf = "wxsender.conf"
        self.initUI()
        self.ui.btBrowser.clicked.connect(self.bt_browser_dir)
        self.ui.btSave.clicked.connect(self.bt_save)

        self.isTrayCreate = False
        self.addSystemTray()

    def initUI(self):
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.ui.txtSndLag.setText("30")
        self.ui.txtSndLagT.setText("60")
        self.ui.txtSndCnt.setText("0")

        # 设置列数
        self.ui.treeWidget.setColumnCount(1)
        # 设置树形控件头部的标题
        self.ui.treeWidget.setHeaderLabels(['群列表'])
        # 设置根节点
        root = QTreeWidgetItem(self.ui.treeWidget)
        root.setText(0, '微信群列表')
        self.grouplist = wxsnd.get_group_list()

        # 设置微信群列表
        for group in self.grouplist:
            child1 = QTreeWidgetItem()
            child1.setText(0, group["NickName"])
            child1.setCheckState(0, not Qt.Checked)
            root.addChild(child1)

        self.ui.treeWidget.expandAll()

        try:
            if os.path.exists(self.save_conf):
                sender_conf = Utils.read_config(self.save_conf)
                if len(sender_conf) != 0:
                    self.set_groups_choosed(sender_conf["groupList"])
                    self.ui.txtWorkdir.setText(sender_conf["workDir"])
                    self.ui.txtSndLag.setText(sender_conf["sndLag"])
                    self.ui.txtSndLagT.setText(sender_conf["sndLagT"])
                    self.ui.txtSndCnt.setText(sender_conf["sndCnt"])
        except Exception as e:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "读取配置文件并配置出错!!:%s" % e,
                                    QMessageBox.Ok)
            return


    def bt_browser_dir(self):
        wkdir = QFileDialog.getExistingDirectory(self,  "选取文件夹", "./")  # 起始路径
        #print(wkdir)
        self.ui.txtWorkdir.setText(wkdir)
        print(self.ui.txtWorkdir.toPlainText())


    def bt_save(self):
        save_info = {}

        workDir = self.ui.txtWorkdir.toPlainText()
        if workDir == "" or not os.path.isdir(workDir):
            QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "请重新选择工作目录!!",
                                    QMessageBox.Ok)
            return

        sndLag = self.ui.txtSndLag.toPlainText()
        if not sndLag.isdigit():
            QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "发送间隔必须为数字!!",
                                    QMessageBox.Ok)
            return

        sndLagT = self.ui.txtSndLagT.toPlainText()
        if not sndLagT.isdigit():
            QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "完成产品发送间隔必须为数字!!",
                                    QMessageBox.Ok)
            return

        sndCnt = self.ui.txtSndCnt.toPlainText()
        if not sndCnt.isdigit():
            QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "产品循环发送次数必须为数字!!",
                                    QMessageBox.Ok)
            return

        print(workDir)

        #self.showMessage()
        groupList = self.get_choosed_groups()
        save_info["groupList"] = groupList
        save_info["workDir"] = workDir
        save_info["sndLag"] = sndLag
        save_info["sndLagT"] = sndLagT
        save_info["sndCnt"] = sndCnt

        try:
            Utils.write_config(self.save_conf, save_info)
        except Exception as e:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "写入配置文件出错!!:%s" % e,
                                    QMessageBox.Ok)
            return
        if not wxsnd.wx_send_flag:
            self.start_sender_thread()
        if not wxsnd.wx_sync_flag:
            self.start_wx_sync_thread()

        self.hide()

    def start_sender_thread(self):
        try:
            if os.path.exists(self.save_conf):
                sender_conf = Utils.read_config(self.save_conf)
                if len(sender_conf) != 0:
                    self.tsnd = threading.Thread(target=wxsnd.send_product_msg, args=(sender_conf, ))
                    self.tsnd.start()
        except Exception as e:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "提示",
                                    "读取配置文件并配置出错!!:%s" % e,
                                    QMessageBox.Ok)
            return

    def start_wx_sync_thread(self):
        self.twxsync = threading.Thread(target=wxsnd.wx_sync)
        self.twxsync.start()

    def get_choosed_group_ids(self, glistn):
        g_namelist = list()
        #print("self.grouplist:%s" % self.grouplist)
        for groupn in glistn:
            for g in self.grouplist:
                if g["NickName"] == groupn:
                    g_namelist.append(g["UserName"])
        return g_namelist

    def set_groups_choosed(self, choosedlist):
        root = self.ui.treeWidget.invisibleRootItem()
        signal_count = root.childCount()
        for gname in choosedlist:
            for i in range(signal_count):
                signal = root.child(i)

                num_children = signal.childCount()
                for n in range(num_children):
                    child = signal.child(n)
                    if child.text(0) == gname:
                        child.setCheckState(0, Qt.Checked)

    def get_choosed_groups(self):
        checked = dict()
        # list_all=[]
        checked_sweeps = list()
        root = self.ui.treeWidget.invisibleRootItem()
        signal_count = root.childCount()
        for i in range(signal_count):
            signal = root.child(i)

            num_children = signal.childCount()
            for n in range(num_children):
                child = signal.child(n)
                if child.checkState(0) == Qt.Checked:
                    checked_sweeps.append(child.text(0))
                    # list_all.append(child.text(0))
                    # list_all.append(str(child.text(0)))

            #checked[signal.text(0)] = checked_sweeps
        # print checked.keys()[0]
        # print checked[checked.keys()[0]]
        return checked_sweeps

    def addSystemTray(self):
        minimizeAction = QAction("关 于", self, triggered=self.aboutme)
        restoreAction = QAction("配置参数", self,
                                triggered=self.showNormal)
        quitAction = QAction("退出程序", self,
                             triggered=self.close)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(minimizeAction)
        self.trayIconMenu.addAction(restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(quitAction)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("icon.png"))
        self.setWindowIcon(QIcon("icon.png"))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.activated.connect(self.iconActivated)  # 触发托盘事件
        self.trayIcon.show()
        self.isTrayCreate = True
        # 触发托盘icon

    def iconActivated(self, reason):
        if reason == 2 or reason == 3:
            self.show()

    def aboutme(self):
        about_ui = AboutGUI()
        #btn = self.ui.pushButton_new
        #btn.clicked.connect(about_ui.show)
        about_ui.exec_()


    def quit(self):
        #保险起见，为了完整的退出
        self.setVisible(False)
        self.parent().exit()
        qApp.quit()
        sys.exit()

    def showMessage(self):
        #icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QSystemTrayIcon.Information)
        self.trayIcon.showMessage("提示",  "程序已运行在后台...",
                                  1, 5 * 1000)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.trayIcon.isVisible():
                self.trayIcon.hide()
            wxsnd.gExit = True
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgLogin = WxLoginGUI()
    dlgLogin.show()
    dlgLogin.exec_()
    if dlgLogin.isLogin:
        MainWindow = SetGUI()

        MainWindow.show()
        sys.exit(app.exec_())
    print("aaaaaaaaaa")