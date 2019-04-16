# -*- coding: utf-8 -*-
import ctypes
import inspect
import json
from configparser import ConfigParser


class Utils(object):

    @staticmethod
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    @staticmethod
    def stop_thread(thread):
        Utils._async_raise(thread.ident, SystemExit)

    @staticmethod
    def read_ini(inifile, section, key):
        cf = ConfigParser.ConfigParser()
        cf.readfp(open(inifile))
        return cf.get(section, key)

    @staticmethod
    def write_ini(inifile, section, key, value):
        cf = ConfigParser.ConfigParser()
        # modify cf, be sure to read!
        cf.read(inifile)
        cf.set(section, key, value)  # set to modify
        # cf.remove_option("test1", "name")
        # write to file
        with open(inifile, "w+") as f:
            cf.write(f)

    @staticmethod
    def write_config(conf, dic):
        with open(conf, "w+") as f:
            json.dump(dic, f)

    @staticmethod
    def read_config(conf):
        with open(conf, "r") as f:
            try:
                dicstr = json.load(f)
            except Exception:
                dicstr = {}

        return dicstr

