#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

"""
agent 入口文件
"""

import os
import uuid
import threading
from queue import Queue
from agent.core.worker import Worker
from agent.core.executor import Executor
from agent.core.codec import Codec

class Agent:
    def __init__(self, host, port, workspace):
        """
        :param host: agent启动IP地址
        :param port: agent启动端口
        :param workspace: agent工作路径
        """
        if not os.path.exists(workspace):   # 判断工作路径是否存在
            os.makedirs(workspace)   # 若不存在则创建工作路径
        if os.path.exists(os.path.join(workspace, '.id')):  # 保存agent id的文件是否存在
            with open(os.path.join(workspace, '.id')) as f:  # 存在则读取
                self.id = f.readline()
        else:
            self.id = uuid.uuid1().hex  # agent id
            with open(os.path.join(workspace, '.id'), 'w') as f:  # 不存在则创建这个文件，并且写入agent id
                f.write(self.id)
        if os.path.exists(os.path.join(workspace, '.pid')):
            with open(os.path.join(workspace, '.pid')) as f:
                pid = f.readline()
                if pid:
                    try:
                        os.kill(int(pid), 0)
                        print("ProcessLookupError: [Errno 1] Process already exists.")
                        os._exit(0)
                    except Exception as e:
                        pid = os.getpid()
                        with open(os.path.join(workspace, '.pid'), 'w') as f:
                            f.write(str(pid))
                else:
                    pid = os.getpid()
                    with open(os.path.join(workspace, '.pid'), 'w') as f:
                        f.write(str(pid))
        else:
            pid = os.getpid()
            with open(os.path.join(workspace, '.pid'), 'w') as f:
                f.write(str(pid))
        queue = Queue()  # 任务队列
        c = Codec(self.id)
        self.worker = Worker((host, port), workspace, queue, c)  # 连接管理模块
        self.executor = Executor(workspace, queue, c, self.worker)  # 执行任务
        self.event = threading.Event()  # 线程事件

    def _supervisor(self):
        """
        :return: socket断开后，自动连接
        """
        while not self.event.is_set():
            self.worker.start()  # 和master建立连接
            self.worker.join()  # 阻塞当前连接线程
            self.event.wait(3)  # 3秒重连一次

    def start(self):
        threading.Thread(name='supervisor', target=self._supervisor, daemon=True).start()  # 单独启动一个重连的线程
        self.executor.start()

    def shutdown(self):
        self.event.set()
        self.executor.shutdown()
