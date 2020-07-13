#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : YuLei Lan
# @File    : __init__.py.py
# @Software: PyCharm

import redis
from conf import REDIS_CONFIG

pool = redis.ConnectionPool(
    host=REDIS_CONFIG.get("host", ""),
    password=REDIS_CONFIG.get("password", ""),
    port=REDIS_CONFIG.get("port", ""),
    decode_responses=True,
)
redis_object = redis.Redis(connection_pool=pool)
