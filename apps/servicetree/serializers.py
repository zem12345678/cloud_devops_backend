from rest_framework import serializers
from .models import Node

class NodeSerializer(serializers.ModelSerializer):
    """
    NodeInfo序列化类
    """

    def validate_pid(self, pid):
        """
        Check that the per_pid is or not parent
        """
        if pid > 0:
            try:
                Node.objects.get(pk=pid)
                return pid
            except Node.DoesNotExist:
                return serializers.ValidationError("上级菜单不存在")
        else:
            return 0

    class Meta:
        model = Node
        fields = ('id', 'name', 'pid', 'path', 'op', 'rd')
        read_only_fields = ('path','id')