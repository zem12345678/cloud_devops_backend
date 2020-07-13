#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

"""
执行动作模块
"""

import json
import os
import base64
import logging
import threading
import subprocess
from queue import Queue, Empty


class Executor:
    def __init__(self, workspace, queue: Queue, codec, worker):
        """
        :param workspace: 工作空间
        :param queue: 执行队列
        :param codec: 返回的状态数据
        """
        self.workspace = workspace
        self.queue = queue
        self.event = threading.Event()
        self.process = None
        self.codec = codec
        self.worker = worker

    def _exec(self, task):
        """ 执行动作 """
        task = json.loads(task.replace("'", '"'))
        task_id = task["task_id"]
        self.codec.current(task_id)  # 当前任务ID
        logging.debug("execute {}".format(task_id))
        script = base64.b64decode(task["script"]).decode()
        self.worker.send(self.codec.result(task_id, "RUNNING", "", task["uuid"]))
        p = subprocess.Popen(
            script,
            shell=True,
            close_fds=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )  # 执行任务
        self.process = p  # subprocess对象
        timeout = task.get("timeout", 0)  # 任务超时时间
        if timeout > 0:
            p.wait(timeout)  # 设置超时时间
        else:
            p.wait()  # 不设置超时时间
        self.process = None  # 任务结束
        logging.debug("execute {} exit with {}".format(task_id, p.returncode))
        self.codec.current(None)  # 解除当前任务的操作
        stdout, stderr = p.communicate() # 获取任务返回
        if p.returncode == 0:
            self.worker.send(self.codec.result(task_id, "SUCCEED", str(stdout, encoding="utf-8"), task["uuid"]))
        else:
            self.worker.send(self.codec.result(task_id, "FAILED", str(stderr, encoding="utf-8"), task["uuid"]))

    def start(self):
        while not self.event.is_set():
            try:
                task = self.queue.get_nowait()  # 获取在队列中等待的任务
                if task:
                    self._exec(task)  # 执行任务
            except Empty:
                pass
            except Exception as e:
                import traceback

                traceback.print_exc()
                logging.error("exec error: {}".format(e))  # 执行失败
                self.codec.current(None)

    def shutdown(self):
        self.event.set()
        if self.process is not None:
            self.process.terminate()  # 结束任务
