# -*- coding: utf-8 -*-
import redis
import time
from django.conf import settings
from utils.wrappers import catch_exception
from cloud_devops_backend.settings import REDIS_HOST,REDIS_DB,REDIS_PORT,REDIS_PASSWORD
locals().update(settings.LOCK)

class RedisLock(object):

    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
    redis_client = redis.Redis(connection_pool=pool)
    timeout = 600

    @classmethod
    def delete_lock(cls, key):
        cls.redis_client.delete(key)

    @classmethod
    @catch_exception
    def set_lock(cls, key, value):
        return cls.redis_client.setnx(key, value)

    @classmethod
    def locked(cls, key):
        now = int(time.time())
        if cls.set_lock(key, now):
            return True
        lock_time = cls.redis_client.get(key)
        if now > int(lock_time) + cls.timeout:
            cls.delete_lock(key)
            return cls.set_lock(key, now)
        return False
