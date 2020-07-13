#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

import os
import sys
import threading
import socket
from logging.config import fileConfig
from configparser import ConfigParser
from service.master import Master


home = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "service/master/conf")
config = ConfigParser()
config.read(os.path.join(home, "config.ini"))
master_host = config.get("master", "host")
master_port = int(config.get("master", "port"))
if os.path.exists(os.path.join(home, "logging.ini")):
    fileConfig(os.path.join(home, "logging.ini"))


def _start_socket():
    """ 启动socket监听 """

    config = ConfigParser()
    config.read(os.path.join(home, "config.ini"))
    master = Master(master_host, master_port)
    try:
        master.start()
    except KeyboardInterrupt:
        master.shutdown()


def _is_port_open():
    """ 判断端口是否被占用 """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((master_host, master_port))
        s.shutdown(2)
        return True
    except:
        return False
    finally:
        s.close()


def thread_service():
    """ 单独开启一个线程启动socket监听端口 """

    if not _is_port_open():
        threading.Thread(name="_start_socket", target=_start_socket, daemon=True).start()


if __name__ == "__main__":
    thread_service()
