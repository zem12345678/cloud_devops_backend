from rest_framework import serializers
from clouds.models import Instances, Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    厂商列化类
    """
    class Meta:
        model = Manufacturer
        fields = '__all__'


class InstanceSerializer(serializers.ModelSerializer):
    """
    主机序列化类
    """
    def to_representation(self, instance):
        ret = super(InstanceSerializer, self).to_representation(instance)
        if instance.vpc_id == "vpc":
            ret['vpc_id'] = "私有网络"
        if instance.instance_charge_type == "PrePaid":
            ret['instance_charge_type'] = "包年包月"
        if instance.ioOptimized == "True":
            ret['ioOptimized'] = "I/O优化"
        ret['cloud_id'] = instance.cloud_id.vendor_name
        return ret

    class Meta:
        model = Instances
        fields = '__all__'


class SlbSerializer(serializers.ModelSerializer):
    """
    主机序列化类
    """
    class Meta:
        model = Instances
        fields = '__all__'
