# @Time    : 2020/7/13 15:45
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from rest_framework import serializers
from ..models import Label
from ..models import DeviceInfo


class LabelSerializer(serializers.ModelSerializer):
    '''
    标签序列化
    '''
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=DeviceInfo.objects.all(), source='deviceinfo_set')
    class Meta:
        model = Label
        fields = '__all__'