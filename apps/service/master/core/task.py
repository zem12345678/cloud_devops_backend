#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

import json
from .state import *
from .lock import lock
from utils.operating_redis import redis_object
from conf import TASK_WAITING
import logging


class Task:
    def __init__(self, task_id="", script="", uuid="", targets=None, timeout=0, parallel=1, fail_rate=0, fail_count=0):
        if targets is None:
            targets = []
        self.id = task_id
        self.script = script
        self.uuid = uuid
        self.timeout = timeout
        self.parallel = parallel
        self.fail_rate = fail_rate
        self.fail_count = fail_count
        self.targets = {x: {"state": WAITING, "output": ""} for x in targets}
        self._state = WAITING
        self.total = len(targets)
        self.tasks = {}

    def put_task(self, task, targets):
        """ 发布任务 """

        if task["task_id"] in self.tasks:
            raise Exception("task {} exist".format(task["task_id"]))
        t = Task(**task, targets=targets)
        self.tasks[t.id] = t

    def get_tasks(self, states=None):
        """ 获取等待和执行中的任务 """
        while True:
            try:
                task_dict = redis_object.rpop(TASK_WAITING)
                if task_dict is None:
                    return self.tasks
                task_dict = json.loads(task_dict)
                task_obj = Task(**task_dict["task"], targets=task_dict["targets"])
                self.tasks[task_obj.id] = task_obj
            except Exception as e:
                logging.error(e)
                break

    def get_task(self, task_id):
        """ 获取一个任务 """

        return self.tasks.get(task_id)

    def set_target_state(self, target_id, state, output=""):
        """ 设置任务状态 """

        with lock:
            self.targets[target_id] = {"state": state, "output": output}

            failed = len([x for x in self.targets.values() if x["state"] == FAILED])
            if failed > self.fail_count >= 0:
                self._state = FAILED

            elif failed / self.total > self.fail_rate >= 0:
                self._state = FAILED

            elif len([x for x in self.targets.values() if x["state"] in {"WAITING", "RUNNING"}]) == 0:
                self._state = SUCCEED

            # TaskList.objects.filter(task_id=self.id).update(state=self._state)

            return

    def state(self, state=None):
        """ 状态 """

        with lock:
            if state is None:
                return self._state
            self._state = state
            return self._state

    def running(self):
        """ 运行中的任务 """

        with lock:
            return len([x for x in self.targets.values() if x["state"] == RUNNING])
