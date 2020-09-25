# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Workflow, Step

class WorkOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow
        fields = '__all__'

class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Step
        fields = '__all__'
