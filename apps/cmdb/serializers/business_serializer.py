# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from rest_framework import serializers
from ..models import Business,DeviceInfo

class BusinessSerializer(serializers.ModelSerializer):
    '''
    业务序列化
    '''
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=DeviceInfo.objects.all(),
                                               source='deviceinfo_set')
    class Meta:
        model = Business
        fields = '__all__'