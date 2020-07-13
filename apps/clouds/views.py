from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from .serializers import ManufacturerSerializer, InstanceSerializer
from .models import Manufacturer, Instances


class ManufacturerViewset(viewsets.ModelViewSet):
    """
    list:
    获取云厂商列表
    update:
    更新云厂商信息
    destroy:
    删除云厂商信息
    create:
    创建云厂商
    partial_update:
    更新云厂商信息
    retrieve:
    获取云厂商详细信息
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class CloudInstanceViewset(mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    list:
    获取实例列表
    destroy:
    删除实例
    retrieve:
    获取实例详细信息
    """
    queryset = Instances.objects.all()
    serializer_class = InstanceSerializer
