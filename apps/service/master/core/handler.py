#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

import json
import logging
import threading
from django.utils import timezone
from .state import *
from socketserver import StreamRequestHandler
from apps.system import models
from django.utils import timezone
from apps.task.models import TaskHistory


class Handler(StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.event = threading.Event()
        self.agent_id = None
        super().__init__(request, client_address, server)

    def _get_register_agent(self):
        """ 获取agent是否存在 """

        agent_count = models.AgentList.objects.filter(agent_id=self.agent_id).count()
        if agent_count == 0:
            return False
        return True

    def _handle_heartbeat(self, payload):
        """ 处理心跳数据 """

        self.agent_id = payload["id"]
        if self._get_register_agent():
            current_time = timezone.now()
            models.AgentList.objects.filter(agent_id=self.agent_id).update(last_heartbeat=current_time)
            info = {"hostname": payload["hostname"], "ip": payload["ip"]}
            agent = self.server.agent.register(self.agent_id, info)
            if payload.get("current_task") is None:
                task = agent.get_agent_task(self.agent_id)
                if task:
                    data = json.dumps({"type": "task", "payload": task})
                    self.wfile.write("{}\r\n".format(data).encode())
                    self.wfile.flush()

    def _handle_register(self, payload):
        """ 处理注册数据 """

        try:
            approval_agent_count = models.AgentApprovalList.objects.filter(agent_id=str(payload["agent_id"])).count()
            agent_count = models.AgentList.objects.filter(agent_id=str(payload["agent_id"])).count()
            if agent_count == 0:
                if approval_agent_count == 0:
                    payload["apply_time"] = timezone.now()
                    models.AgentApprovalList.objects.create(**payload)
        except Exception as e:
            logging.error(e)

    def _handle_result(self, payload):
        """ 处理返回数据 """

        self.agent_id = payload["agent_id"]
        if self._get_register_agent():
            if payload["code"] == RUNNING:
                history_value = {
                    "status": RUNNING,
                    "start_time": timezone.now()
                }
            else:
                history_value = {
                    "status": payload["code"],
                    "end_time": timezone.now()
                }
            history_value["content"] = payload["output"]
            TaskHistory.objects.filter(agent=self.agent_id, uuid=payload["uuid"]).update(**history_value)

    def _handle(self):
        """ 获取并判断agent发送过来的数据类型 """

        try:
            data = self.rfile.readline().strip()
            if not data:
                return
            msg = json.loads(data.decode())
            if msg.get("type") == "register":
                self._handle_register(msg["payload"])

            if msg.get("type") == "heartbeat":
                self._handle_heartbeat(msg["payload"])

            if msg.get("type") == "result":
                self._handle_result(msg["payload"])
        except Exception as e:
            logging.error("handle agent connection error: {}".format(e))
            self.event.set()

    def handle(self):
        """ 执行handle """

        try:
            while not self.event.is_set():
                self._handle()
        except KeyboardInterrupt:
            return

    def finish(self):
        """ 提交 """

        super().finish()
        if getattr(self, "event"):
            self.event.set()
