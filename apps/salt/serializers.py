from rest_framework import serializers
from .models import MinionsStatus, SaltAcl, SaltMdl, SaltSls, SaltArg, CmdHistory
import django.utils.timezone as timezone


class MinionStausSerializer(serializers.Serializer):
    """
    Minion状态序列化类
    """
    minion_id = serializers.CharField(max_length=32, label="主机名", help_text="主机名", read_only=True)
    minion_status = serializers.CharField(required=True, max_length=32, label="minion状态", help_text="minion状态")

    class Meta:
        model = MinionsStatus
        fields = '__all__'


class AclSerializer(serializers.ModelSerializer):
    """
    Minion状态序列化类
    """
    name = serializers.CharField(max_length=64, required=True, label="ACL名称", help_text="ACL名称")
    description = serializers.CharField(max_length=128, default="请添加描述", label="ACL描述", help_text="ACL描述")
    deny = serializers.CharField(max_length=64, required=True, label="拒绝名称", help_text="拒绝名称")
    add_time = serializers.DateTimeField(read_only=True, default=timezone.now)

    class Meta:
        model = SaltAcl
        fields = '__all__'


class SlsSerializer(serializers.ModelSerializer):
    """
    salt状态文件序列化类
    """
    name = serializers.CharField(max_length=64, required=True, label="sls名称", help_text="sls名称")
    description = serializers.CharField(max_length=128, default="请添加描述", label="状态文件描述", help_text="状态文件描述")
    add_time = serializers.DateTimeField(read_only=True, default=timezone.now)

    class Meta:
        model = SaltSls
        fields = '__all__'


class MdlSerializer(serializers.ModelSerializer):
    """
    salt模块序列化类
    """
    name = serializers.CharField(max_length=64, required=True, label="mdl名称", help_text="mdl名称")
    description = serializers.CharField(max_length=128, default="请添加描述", label="模块描述", help_text="模块描述")
    add_time = serializers.DateTimeField(read_only=True, default=timezone.now)

    class Meta:
        model = SaltMdl
        fields = '__all__'


class ArgSerializer(serializers.ModelSerializer):
    """
    salt模块序列化类
    """
    name = serializers.CharField(max_length=64, required=True, label="cmd.run模块参数名称", help_text="cmd.run模块参数名称")
    description = serializers.CharField(max_length=128, default="请添加描述", label="参数描述", help_text="参数描述")
    add_time = serializers.DateTimeField(read_only=True, default=timezone.now)

    class Meta:
        model = SaltArg
        fields = '__all__'


class CmdHistorySerializer(serializers.ModelSerializer):
    """
    commond命令历史记录序列化类
    """
    execute_time = serializers.DateTimeField(read_only=True, default=timezone.now)

    class Meta:
        model = CmdHistory
        fields = '__all__'
