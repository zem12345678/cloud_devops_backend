from rest_framework import serializers
from .models import Tasks

class TasksSerializer(serializers.ModelSerializer):
    """
    任务序列化类
    """

    class Meta:
        model = Tasks
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance
