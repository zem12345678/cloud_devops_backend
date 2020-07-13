#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

import base64
import datetime
import json
from apps.system.models import AgentList
from utils.operating_redis import redis_object


class Agent:
    def __init__(self, agent_id="", info=None):
        self.id = agent_id
        self.last_heartbeat = datetime.datetime.now()
        self.info = info
        self.queue = []
        self.tasks = {}
        self.agents = {}

    def heartbeat(self, info):
        """ 心跳消息 """

        self.info = info
        self.last_heartbeat = datetime.datetime.now()

    def register(self, agent_id, info):
        """ agent注册 """

        agent = Agent(agent_id, info)
        agent.heartbeat(info)
        return agent

    def get_agent(self, agent_id):
        """ 获取agent对象 """

        agent_obj = AgentList.objects.get(agent_id=agent_id)
        info = {
            "hostname": agent_obj.hostname,
            "ip": agent_obj.ipaddress,
        }
        return Agent(agent_id, info)

    def get_agent_task(self, agent_id):
        """ 获取agent任务 """

        task = redis_object.rpop(agent_id)
        return task

    def send(self, task, agent_id):
        """ 给agent发送任务 """

        payload = {
            "task_id": task.id,
            "uuid": task.uuid,
            "script": base64.b64encode(task.script.encode()).decode(),
            "timeout": task.timeout,
        }
        # redis_object.rpush("dispatch_task_id", task.id)
        redis_object.lpush(agent_id, json.dumps(payload))

    def free(self, task_id):
        """ agent修改为空闲状态 """

        try:
            self.queue.remove(task_id)
            self.tasks.pop(task_id)
        except Exception as e:
            pass
