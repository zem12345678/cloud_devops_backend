# @Time    : 2020/7/13 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from rest_framework import serializers
from ..models import ConnectionInfo

class ConnectionInfoSerializer(serializers.ModelSerializer):
    '''
    连接密码信息序列化
    '''
    uid_name = serializers.ReadOnlyField(source='uid.name')

    class Meta:
        model = ConnectionInfo
        fields = '__all__'