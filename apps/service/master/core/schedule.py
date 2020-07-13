#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

import logging
import threading
from .state import *


class Scheduler:
    def __init__(self, agent, task):
        self.agent = agent
        self.task = task
        self.event = threading.Event()

    def _schedule(self):
        """ 任务调度 """

        tasks = self.task.get_tasks()
        if tasks:
            for task_id in tasks:
                task = tasks.get(task_id, None)
                if task:
                    for _ in range(task.parallel - task.running()):
                        for agent_id, target in task.targets.items():
                            if target["state"] == WAITING:
                                agent = self.agent.get_agent(agent_id)
                                if agent is None:
                                    logging.error("agent {} not exist".format(agent_id))
                                    task.set_target_state(agent_id, FAILED, "agent {} not exist".format(agent_id))
                                    continue
                                agent.send(task, agent_id)
                                task.set_target_state(agent_id, RUNNING)

    def _run(self):
        """ 设置任务调度 """

        while not self.event.is_set():
            self._schedule()
            self.event.wait(3)  # 3秒钟调度一次

    def start(self):
        """ 单独开启一个线程启动任务调度 """

        threading.Thread(name="scheduler", target=self._run, daemon=True).start()

    def shutdown(self):
        """ 停止任务调度 """

        self.event.set()
