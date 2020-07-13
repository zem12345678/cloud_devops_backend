# @Time    : 2020/7/13 15:45
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm
from rest_framework import serializers
from ..models import DeviceScanInfo

class DeviceScanInfoSerializer(serializers.ModelSerializer):
    '''
    扫描信息序列化
    '''
    class Meta:
        model = DeviceScanInfo
        fields = '__all__'

class DeviceScanListSerializer(serializers.ModelSerializer):
    '''
    扫描信息列表序列化
    '''
    class Meta:
        model = DeviceScanInfo
        fields = ('id','sys_hostname','hostname','auth_type','os_type','status')