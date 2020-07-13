# @Time    : 2020/7/13 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm


from rest_framework import serializers
from ..models import Dict

class DictSerializer(serializers.ModelSerializer):
    '''
    字典序列化
    '''
    class Meta:
        model = Dict
        fields = '__all__'

class DictTreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='value')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)