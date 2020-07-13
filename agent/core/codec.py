#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

import json
import threading
import netifaces
import ipaddress
import socket


def _encode(msg):
    return "{}\r\n".format(json.dumps(msg))


class Codec:
    def __init__(self, agent_id):
        self.id = agent_id
        self._current_task = None
        self.lock = threading.Lock()

    def _get_addresses(self):
        """ 获取agent的所有IP地址 """
        addresses = []
        for iface in netifaces.interfaces():
            try:
                for nets in netifaces.ifaddresses(iface).values():
                    for net in nets:
                        try:
                            addr = ipaddress.ip_address(net["addr"])
                        except Exception as e:
                            continue
                        if addr.is_loopback:
                            continue
                        if addr.is_link_local:
                            continue
                        if addr.is_multicast:
                            continue
                        addresses.append(str(addr))
            except Exception as e:
                pass
        return addresses

    def register(self):
        """ agent注册 """
        return _encode(
            {
                "type": "register",
                "payload": {"agent_id": self.id, "hostname": socket.gethostname(), "ipaddress": self._get_addresses()},
            }
        )

    def current(self, task_id):
        """ 设置当前任务ID """
        with self.lock:
            self._current_task = task_id

    def heartbeat(self):
        """ 心跳数据 """
        with self.lock:
            return _encode(
                {
                    "type": "heartbeat",
                    "payload": {
                        "id": self.id,
                        "hostname": socket.gethostname(),
                        "ip": self._get_addresses(),
                        "current_task": self._current_task,
                    },
                }
            )

    def result(self, task_id, code, output, uuid):
        """ 任务执行完成后，返回的数据 """
        return _encode(
            {
                "type": "result",
                "payload": {"agent_id": self.id, "task_id": task_id, "code": code, "output": output, "uuid": uuid},
            }
        )
