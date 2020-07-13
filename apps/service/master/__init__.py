#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

"""
master入口文件
"""

import threading
from service.master.core.task import Task
from service.master.core.agent import Agent
from service.master.core.handler import Handler
from service.master.core.schedule import Scheduler
from socketserver import ThreadingTCPServer


class Master:
    def __init__(self, master_host, master_port):
        self.server = ThreadingTCPServer((master_host, master_port), Handler)
        agent = Agent()
        self.server.agent = agent
        task = Task()
        self.server.task = task
        self.scheduler = Scheduler(agent, task)
        self.event = threading.Event()

    def start(self):
        self.scheduler.start()
        threading.Thread(name='master', target=self.server.serve_forever, daemon=True).start()
        self.event.wait()

    def shutdown(self):
        self.server.shutdown()
        self.scheduler.shutdown()
        self.event.set()

