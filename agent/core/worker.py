#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

"""
socket连接模块
"""

import os
import sys
import json
import shutil
import socket
import logging
import threading
import time
import redis


class Worker:
    def __init__(self, master, workspace, queue, codec):
        """
        :param master: master连接地址
        :param workspace: agent工作空间
        :param queue: 任务队列
        :param codec: 状态信息
        """
        self.master = master
        self.so = None
        self.rfile = None
        self.wfile = None
        self.workspace = workspace
        self.queue = queue
        self.codec = codec
        self.event = threading.Event()
        self.agent_id = ""

    def _register(self):
        """ 发送注册消息 """
        self._send(self.codec.register())

    def _heartbeat(self):
        """ 每3秒发送一次心跳消息 """
        while not self.event.is_set():
            self._send(self.codec.heartbeat())
            self.event.wait(3)

    def _dispatch(self):
        """ 调度任务 """
        while not self.event.is_set():
            try:
                msg = self.rfile.readline().strip()
                if not msg:
                    continue
                message = json.loads(msg)
                if message.get("type") == "task":
                    task = message["payload"]
                    task_id = json.loads(task.replace("'", '"')).get("task_id", None)
                    if task_id is not None:
                        self.queue.put(task)
                    else:
                        continue

            except Exception as e:
                logging.error("exec error {}".format(e))
                self.shutdown()
            time.sleep(1)

    def _send(self, msg):
        try:
            self.wfile.write(msg)
            self.wfile.flush()
        except Exception as e:
            logging.error("send message error: {}".format(e))
            self.shutdown()

    def send(self, msg):
        self._send(msg)

    def _connect(self):
        """ 建立socket连接 """
        try:
            self.event.clear()
            self.so = socket.socket()  # socket连接对象
            self.so.connect(self.master)  # 连接master
            self.rfile = self.so.makefile(mode="r")  # 读权限的socket文件对象
            self.wfile = self.so.makefile(mode="w")  # 写权限的socket文件对象
        except Exception as e:
            logging.error("connect to master {}:{} error: {}".format(*self.master, e))
            self.shutdown()

    def start(self):
        """ 启动agent """
        self._connect()  # 建立链接
        self._register()
        threading.Thread(name="heartbeat", target=self._heartbeat, daemon=True).start()
        threading.Thread(name="dispatch", target=self._dispatch, daemon=True).start()

    def shutdown(self):
        """ 关闭连接 """
        self.event.set()
        if self.rfile:
            self.rfile.close()
        if self.wfile:
            self.wfile.close()
        if self.so:
            self.so.close()

    def join(self):
        self.event.wait()
