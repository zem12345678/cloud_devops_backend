from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import WorkOrder

User = get_user_model()


class WorkOrderSerializer(serializers.ModelSerializer):
    """
    工单序列化类
    """
    # 获取当前登陆用户，并将其赋值给数据库中对应的字段
    applicant = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    # apply_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # complete_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = WorkOrder
        fields = "__all__"

    def to_representation(self, instance):
        applicant_obj = instance.applicant
        assign_to_obj = instance.assign_to
        final_processor_obj = instance.final_processor
        type_value = instance.get_type_display()
        status_value = instance.get_status_display()
        ret = super(WorkOrderSerializer, self).to_representation(instance)
        ret['type'] = {
             "id": instance.type,
             "name": type_value
        }
        ret['status'] = {
            "id": instance.status,
            "name": status_value
        }
        ret["applicant"] = {
                               "id": applicant_obj.id,
                               "name": applicant_obj.name
                           },
        ret["assign_to"] = {
                               "id": assign_to_obj.id,
                               "name": assign_to_obj.name
                           },
        if final_processor_obj:
            ret["final_processor"] = {
                                "id": final_processor_obj.id,
                                "name": final_processor_obj.name
                            },
        # print(ret)
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


