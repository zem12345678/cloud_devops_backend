from rest_framework import serializers


from .models import BasicTicketTemplate 
from .models import TicketDetail 

class BasicTicketTemplateSerializer(serializers.ModelSerializer):

	class Meta:
		model = BasicTicketTemplate 
		fields = '__all__'

	# 字段验证
	def validate(self, attrs):
		print("validate attrs: {}".format(attrs))
		print(type(attrs['status']))
		if attrs['status'] < 0:
			raise serializers.ValidationError('工单状态异常.')
		return attrs

	# def create(self, validated_data):
	# 	data = super(TicketSerializer, self).create(validated_data)
	def to_representation(self, instance):
		ret = super(BasicTicketTemplateSerializer, self).to_representation(instance)	
		return ret 



class TicketDetailSerializer(serializers.ModelSerializer):

        class Meta:
                model = TicketDetail 
                fields = '__all__'
