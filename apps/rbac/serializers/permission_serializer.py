# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from rest_framework import serializers
from ..models import Permission
from django.contrib.auth.models import Permission as AuthPermission,ContentType

class PermissionListSerializer(serializers.ModelSerializer):
    '''
    权限列表序列化
    '''
    menuname = serializers.ReadOnlyField(source='menus.name')

    class Meta:
        model = Permission
        fields = ('id','name','method','menuname','pid')

class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = "__all__"


class AuthPermissionSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()
    status       = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = AuthPermission
        fields = ("id", "content_type", "name", "codename", "status")