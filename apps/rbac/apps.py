# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from django.apps import AppConfig


class RbacConfig(AppConfig):
    name = 'rbac'
    verbose_name = "用户管理"

    def ready(self):
        from .signals import create_user
