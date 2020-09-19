# @Time    : 2020/9/19 18:50
# @Author  : ZhangEnmin
# @FileName: pms_serializer.py
# @Software:

import uuid
from rest_framework import serializers
from ..models import PerAppName, PmsPermission, NodeInfo

class PerAppNameSerializer(serializers.Serializer):
    """
    AppName序列化类
    """
    id = serializers.IntegerField(read_only=True)
    app_key = serializers.CharField(max_length=64, label="APP权限UUID", read_only=True, help_text="APP权限UUID",
                                    error_messages={"blank": "这个字段不能为空", "require": "这个字段是必须的"})
    app_name = serializers.CharField(required=True, max_length=32, label="APP名称", help_text="APP名称",
                                     error_messages={"blank": "这个字段不能为空", "require": "这个字段是必须的"})
    app_desc = serializers.CharField(max_length=32, label="APP应用描述", help_text="APP应用描述")

    def validate_app_name(self, value):
        if self.context['request']._request.method == 'POST':
            if PerAppName.objects.filter(app_name=value).exists():
                ret = {
                    "status": 1,
                    "msg": value + " exists"
                }
                raise serializers.ValidationError(ret)
            return value

    def create(self, validated_data):
        validated_data['app_key'] = uuid.uuid1()
        return PerAppName.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data.get('app_name', instance.app_name))
        instance.app_name = validated_data.get('app_name', instance.app_name)
        instance.save()
        return instance

class AuthPerSerializer(serializers.Serializer):
    """
    权限验证序列化类
    """
    app_name = serializers.CharField(help_text="APP权限名称")
    app_key = serializers.CharField(help_text="APP权限UUID")

class NodeInfoSerializer(serializers.ModelSerializer):
    """
    NodeInfo序列化类
    """

    def to_representation(self, instance):
        ret = super(NodeInfoSerializer, self).to_representation(instance)
        return ret

    def validate_pid(self, pid):
        """
        Check that the per_pid is or not parent
        """
        if pid > 0:
            try:
                node_obj = NodeInfo.objects.get(pk=pid)
                if node_obj.pid != 0 or node_obj:
                    # return serializers.ValidationError("上级菜单错误")
                    return pid
            except NodeInfo.DoesNotExist:
                return serializers.ValidationError("上级菜单不存在")
            return pid
        else:
            return 0

    def update(self, instance, validated_data):
        instance.node_name = validated_data.get("node_name", instance.node_name)
        instance.pid = validated_data.get("pid", instance.pid)
        instance.path_node = validated_data.get("path_node", instance.path_node)
        instance.save()
        return instance

    class Meta:
        model = NodeInfo
        fields = ('id', 'node_name', 'pid', 'path_node')

class PmsPermissionSerializer(serializers.ModelSerializer):

    def validate_codename(self, codename):
        try:
            PmsPermission.objects.get(codename=codename)
            return serializers.ValidationError("名称已存在")
        except PmsPermission.DoesNotExist:
            return codename

    class Meta:
        model = PmsPermission
        fields = ("id", "codename", "desc", "app")



