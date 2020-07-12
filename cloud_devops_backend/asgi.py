# @Time    : 2020/7/12 14:21
# @Author  : ZhangEnmin
# @FileName: asgi.py
# @Software: PyCharm

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud_devops_backend.settings")
django.setup()
application = get_default_application()
