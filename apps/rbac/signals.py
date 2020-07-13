# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
# 注册一个信号，在创建用户时自动加密密码
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
