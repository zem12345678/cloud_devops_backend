from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Deploy

User = get_user_model()


class DeploySerializer(serializers.ModelSerializer):
    """
    工单序列化类
    """
    # 获取当前登陆用户，并将其赋值给数据库中对应的字段
    applicant = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    # apply_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # complete_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Deploy
        fields = "__all__"

    def to_representation(self, instance):
        applicant_obj = instance.applicant
        reviewer_obj = instance.reviewer
        assign_to_obj = instance.assign_to
        status_value = instance.get_status_display()
        ret = super(DeploySerializer, self).to_representation(instance)
        ret['status'] = {
            "id": instance.status,
            "name": status_value
        }
        ret["applicant"] = {
                               "id": applicant_obj.id,
                               "name": applicant_obj.name
                           },
        ret["reviewer"] = {
                               "id": reviewer_obj.id,
                               "name": reviewer_obj.name
                           },

        if assign_to_obj:
            ret["assign_to"] = {
                                   "id": assign_to_obj.id,
                                   "name": assign_to_obj.name
                               },
        return ret

    # def create(self, validated_data):
    #     # applicant = self.context['request'].user   #获取用户信息
    #     print(validated_data)
    #     instance = self.Meta.model.objects.create(**validated_data)
    #     instance.save()
    #     return instance

    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     instance = self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
    #     return instance


