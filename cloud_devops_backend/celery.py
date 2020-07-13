# @Time    : 2020/7/12 14:25
# @Author  : ZhangEnmin
# @FileName: celery.py
# @Software: PyCharm


from __future__ import absolute_import, unicode_literals
import os
from celery import  Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_devops_backend.settings') # 设置django环境

from django.conf import settings
app = Celery('cloud_devops_backend')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(settings.INSTALLED_APPS) # 自动发现task，这个配置会自动从每个app目录下去发现tasks.py文件

# 以下内容也可以写在settings.py文件中