# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from rest_framework import serializers
from ..models import Menu


class MenuSerializer(serializers.ModelSerializer):
    '''
    菜单序列化
    '''

    class Meta:
        model = Menu
        fields = ('id', 'name', 'icon', 'path', 'is_show','is_frame', 'sort', 'component', 'pid')
        extra_kwargs = {'name': {'required': True, 'error_messages': {'required': '必须填写菜单名'}}}
