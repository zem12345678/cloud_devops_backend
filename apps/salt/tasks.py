#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import importlib
import django
import logging
from salt.api import SaltAPI
from salt.models import MinionsStatus

logger = logging.getLogger("error")
# pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, pathname)
# sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud_devops_backend.settings")
# importlib.reload(sys)
# django.setup()

# from celery import Celery
# from cloud_devops_backend.settings import BROKER_URL, CELERY_RESULT_BACKEND
#
# app = Celery('task', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
from cloud_devops_backend.celery import app

@app.task
def minion_status():
    sapi = SaltAPI()
    minions_status = sapi.runner("manage.status")

    for minion_id in minions_status['up']:
        hostname = MinionsStatus()
        try:
            res = MinionsStatus.objects.filter(minion_id=minion_id)
            if not res:
                hostname.minion_id = minion_id
                hostname.minion_status = "up"
                hostname.save()
        except Exception as e:
            logger.error(e.args)
    for minion_id in minions_status['down']:
        hostname = MinionsStatus()
        try:
            res = MinionsStatus.objects.filter(minion_id=minion_id)
            if not res:
                hostname.minion_id = minion_id
                hostname.minion_status = "down"
                hostname.save()
        except Exception as e:
            logger.error(e.args)
            pass


minion_status()
