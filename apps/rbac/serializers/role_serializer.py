# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from rest_framework import serializers
from ..models import Role

class RoleListSerializer(serializers.ModelSerializer):
    '''
    角色序列化
    '''
    class Meta:
        model = Role
        fields = '__all__'
        #depth = 1

class RoleModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        #extra_kwargs = {'menus': {'required': True, 'error_messages': {'required': '必须填写菜单名'}}}

    # def validate_menus(self, menus):
    #     if not menus:
    #         raise serializers.ValidationError('必须选择菜单')
    #     return menus