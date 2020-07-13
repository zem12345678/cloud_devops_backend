from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    """
    项目序列化类
    """
    name = serializers.CharField()
    # def to_representation(self, instance):
    #     ret = {}
    #     ret["role"] = 1
    #     return ret


