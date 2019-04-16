# -*- coding: UTF-8 -*-

import webbrowser
import threading
import time
import sys
import os
import requests
import random

from pywxclient.core.api import WeChatAPI
from pywxclient.core import Session, SyncClient, TextMessage, ImageMessage, parse_message
from pywxclient.core.contact import WechatContact
from pywxclient.contrib.file import LocalFile, HTTPFile

from pywxclient.core.exception import (
    WaitScanQRCode, RequestError, APIResponseError, SessionExpiredError,
    AuthorizeTimeout, UnsupportedMessage)

#from PIL import Image
#import matplotlib.pyplot as plt


class wxsender(object):

    def __init__(self):
        self.isStop = False
        self.gExit = False
        self.wx_send_flag = False
        self.wx_sync_flag = False

    def file_ext(self, path):
        #取文件扩展名
        return os.path.splitext(path)[1]

    def get_choosed_group_ids(self, glistn):
        g_namelist = list()
        #print("self.grouplist:%s" % self.grouplist)
        for groupn in glistn:
            for g in self.grouplist:
                if g["NickName"] == groupn:
                    g_namelist.append(g["UserName"])
        return g_namelist

    def send_product_msg(self, sender_conf):
        touserlist = self.get_choosed_group_ids(sender_conf["groupList"])
        workdir = sender_conf["workDir"]
        sndLag = sender_conf["sndLag"]
        sndLagT = sender_conf["sndLagT"]
        sndCnt = sender_conf["sndCnt"]
        if int(sndCnt) != 0:
            sndCntF = int(sndCnt)
        else:
            sndCntF = 1
        time.sleep(10)
        print("send_product_msg...")
        self.wx_send_flag = True
        #循环发送
        while not self.gExit and sndCntF != 0:
            try:
                print("thread_send_image waiting...")

                products = os.listdir(workdir)
                print(products)

                for d in products:
                    product_dir = "%s/%s" % (workdir, d)
                    for file in os.listdir(product_dir):
                        #发送图片消息
                        if not self.file_ext(file) == ".txt":
                            pic_fullpath = "%s/%s" % (product_dir, file)
                            file_obj = LocalFile(pic_fullpath)
                            for touser in touserlist:
                                media_id = self.c1.upload(file_obj, touser)
                                print("media_id:%s" % media_id)
                                print("touser:%s" % touser)
                                print("fromuser:%s" % self.c1.user['UserName'])
                                msg = ImageMessage(
                                    self.c1.user['UserName'], touser, media_id)
                                self.c1.send_message(msg)
                            time.sleep(1)

                    # 发送文字消息
                    msg_fullpath = "%s/msg.txt" % (product_dir)
                    with open(msg_fullpath, 'r') as f:
                        lines = f.readlines()
                    msg_send = ""
                    for msg_t in lines:
                        print("msg_t:%s" % msg_t)
                        msg_send += msg_t
                    for touser in touserlist:
                        msg = TextMessage(
                            self.c1.user['UserName'], touser, msg_send)
                        self.c1.send_message(msg)
                    print("thread_send_image sending complete:%s..." % product_dir)
                    time.sleep(int(sndLag))
                if sndCnt != 0:
                    sndCntF -= 1;
                time.sleep(int(sndLagT))
            except APIResponseError as e:
                print("error:APIResponseError:%s" % e)
                break
        print ("thread_send_image exit")
        self.wx_send_flag = False

    def get_login_qrcode_pic(self):
        self.s1 = Session()
        self.c1 = SyncClient(self.s1)
        qrcodeurl = self.c1.get_authorize_url()
        #filename = os.path.basename(qrcodeurl)
        qr_pic = requests.get(qrcodeurl)

        return qr_pic.content

    def waitting_for_login(self):
        ret = 2
        while not self.isStop:
            try:
                authorize_success = self.c1.authorize()
            except WaitScanQRCode:
                continue
            except AuthorizeTimeout:
                print('Waiting for authorization timeout.')
                ret = 1
                break
            if authorize_success:
                ret = 0
                break

            print('Waiting for authorization...')
            time.sleep(2)
        return ret

    def get_group_list(self):
        ret_login = self.c1.login()
        # print("ret_login:%s" % ret_login)
        user_list = self.c1.get_contact()
        #print("contacts:%s" % user_list)
        contact = WechatContact(user_list)
        #print("contact.group_contacts:%s" % contact.group_contacts)
        self.grouplist = contact.group_contacts
        return self.grouplist

    def wx_sync(self):
        self.wx_sync_flag = True
        while not self.gExit:
            try:
                print('wx_sync....')
                sync_ret = self.c1.sync_check()
                if sync_ret != 0:
                    msgs = self.c1.sync_message()
                    for msg in msgs['AddMsgList']:
                        try:
                            print(msg)
                            msg_obj = parse_message(msg)
                        except UnsupportedMessage:
                            print('unsupported message %s' % msg)
                            continue
                        else:
                            print(
                                'receive message:%s to %s %s:\n %s' % (
                                msg["FromUserName"], msg["ToUserName"], msg["MsgType"], msg_obj.message))
                    self.c1.flush_sync_key()
            except (RequestError, APIResponseError) as e:
                print('api error.%s' % e)
            except SessionExpiredError:
                print('wechat session is expired....')
                self.gExit = True
                break
            except Exception:
                continue
        self.wx_sync_flag = False

    '''
    @staticmethod
    def test():
        global gExit
        s1 = Session()
        c1 = SyncClient(s1)
        qrcodeurl = c1.get_authorize_url()  # Open the url in web browser

        #t = threading.Thread(target=yerdingwx.thread_open_webbrowser, args=(qrcodeurl, ))
        #t.start()

        filename = os.path.basename(qrcodeurl)
        qr_pic = requests.get(qrcodeurl)
        with open("%s.jpg" % filename, "wb") as code:
            code.write(qr_pic.content)

        img = Image.open('%s.jpg' % filename)
        plt.figure("扫二维码后自动登录,一尔丁专用!!!!!")
        plt.ion()
        plt.axis('off')
        plt.imshow(img)
        plt.show()
        while True:
            try:
                plt.pause(2)
                authorize_success = c1.authorize()
            except WaitScanQRCode:
                continue
            except AuthorizeTimeout:
                print('Waiting for authorization timeout.')
                sys.exit(0)

            if authorize_success:
                break

            print('Waiting for authorization...')
            time.sleep(2)
        plt.ioff()  # 显示完后一定要配合使用plt.ioff()关闭交互模式，否则可能出奇怪的问题

        plt.clf()  # 清空图片
        plt.close()

        ret_login = c1.login()
        #print("ret_login:%s" % ret_login)
        user_list = c1.get_contact()
        #print("contacts:%s" % user_list)
        contact = WechatContact(user_list)
        #print (contact.personal_contacts)
        ray_id = ""
        for per in contact.personal_contacts:
            if per['NickName'] == "一尔丁小助手":
                ray_id = per['UserName']
                break
        print(ray_id)
        #print (contact.mp_contacts)
        #print (contact.group_contacts)
        t1 = threading.Thread(target=yerdingwx.thread_send_image, args=(c1, ray_id,))
        t1.start()

        while True:
            try:
                sync_ret = c1.sync_check()
                if sync_ret != 0:
                    msgs = c1.sync_message()
                    for msg in msgs['AddMsgList']:
                        try:
                            print(msg)
                            msg_obj = parse_message(msg)
                        except UnsupportedMessage:
                            print('unsupported message %s'% msg)
                            continue
                        else:
                            print(
                                'receive message:%s to %s %s:\n %s'%(msg["FromUserName"], msg["ToUserName"], msg["MsgType"], msg_obj.message))
                    c1.flush_sync_key()
            except (RequestError, APIResponseError):
                print('api error.%s' % APIResponseError)
            except SessionExpiredError:
                print('wechat session is expired....')
                gExit = True
                break

            time.sleep(1)

        gExit = True
        t1.join()
    '''
if __name__ == '__main__':
    #yerdingwx.test()
    pass
