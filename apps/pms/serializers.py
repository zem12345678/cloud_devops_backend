import uuid
from rest_framework import serializers
from .models import PerAppName, Permission


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


class PermissionSerializer(serializers.ModelSerializer):

    def validate_codename(self, codename):
        try:
            Permission.objects.get(codename=codename)
            return serializers.ValidationError("名称已存在")
        except Permission.DoesNotExist:
            return codename

    class Meta:
        model = Permission
        fields = ("id", "codename", "desc", "app")
