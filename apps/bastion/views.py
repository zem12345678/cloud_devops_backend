#coding:utf-8
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from apps.bastion import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from apps.bastion.serializers import AccountSerializer,GroupsSerializer,PermissionSerializer,AuditorSerializer
from apps.bastion.filter import AccountFilter,PermissionFilter,AuditorFilter

class AccountView(generics.ListCreateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = AccountFilter


class AccountRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Account.objects.all()
    serializer_class = AccountSerializer
    def delete(self,request,*args,**kwargs):
        username = kwargs.get("username")
        models.Permisssion.objects.filter(username=username).delete()
        models.Account.objects.filter(username=username).delete()
        return Response({"status":"delete ok"})



class PermissionView(generics.ListCreateAPIView):
    queryset = models.Permisssion.objects.order_by("-pk")
    serializer_class = PermissionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PermissionFilter




class PermissionRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Permisssion.objects.order_by("-pk")
    serializer_class = PermissionSerializer



class AuditView(generics.ListCreateAPIView):

    queryset = models.Auditor.objects.order_by("-pk")
    serializer_class = AuditorSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = AuditorFilter

# Create your views here.


class GroupView(generics.ListCreateAPIView):

    queryset = models.Groups.objects.order_by("-pk")
    serializer_class = GroupsSerializer