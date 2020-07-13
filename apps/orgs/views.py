from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .models import Organization
from .serializers import GroupSerializer, GroupMembersSerizlizer, GroupPermissionSerizlizer
from users.serializers import UserSerializer
from pms.serializers import PermissionSerializer
from .filter import OrgFilter
from django.db.models import Q
from django.contrib.auth import get_user_model
from groups.common import get_user_obj, get_permission_obj

User = get_user_model()


class GroupViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    list: 获取角色列表
    create: 添加角色
    retrieve: 查看角色名称
    update: 修改角色名称
    partial_update: 修改角色名称
    destroy: 删除角色名称
    """
    queryset = Organization.objects.all()
    serializer_class = GroupSerializer
    filter_class = OrgFilter
    filter_fields = ['name']

    def get_queryset(self):
        queryset = super(GroupViewset, self).get_queryset()
        queryset = queryset.order_by('id')
        return queryset

class GroupMembersViewset(viewsets.GenericViewSet):
    """
    retrieve: 返回指定角色的成员列表
    update: 往指定角色里添加成员
    destroy: 从指定角色里删除成员
    """
    serializer_class = GroupMembersSerizlizer
    queryset = Organization.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        queryset = self.filter_queryset(instance.user_set.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.user_set.add(*serializer.data["uids"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.user_set.remove(*serializer.data["uids"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupPermissionViewset(viewsets.GenericViewSet):
    """
    retrieve: 返回指定角色的权限列表
    update: 向指定角色里添加权限
    partial_update: 向指定角色里添加权限
    destroy: 从指定角色里删除权限
    """
    queryset = Organization.objects.all()
    serializer_class = GroupPermissionSerizlizer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        queryset = self.filter_queryset(instance.pms_group.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PermissionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PermissionSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.pms_group.add(*serializer.data["pids"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.pms_group.remove(*serializer.data["pids"])
        return Response(status=status.HTTP_204_NO_CONTENT)
