# @Time    : 2020/9/19 19:58
# @Author  : ZhangEnmin
# @FileName: group.py
# @Software: PyCharm

from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from django.contrib.auth import get_user_model
from cloud_devops_backend.basic import OpsResponse
from ..common import get_user_obj, get_permission_obj
from ..filters import GroupFilter
from ..serializers.group_serializer import GroupSerializer, GroupMembersSerizlizer, GroupPermissionSerizlizer
from ..serializers.user_serializer import UserInfoListSerializer
from ..serializers.pms_serializer import PmsPermissionSerializer
from ..models import UserProfile

class GroupViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    list: 获取用户组列表
    create: 添加组
    retrieve: 查看组名称
    update: 修改组名称
    partial_update: 修改组名称
    destroy: 删除组名称
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    filter_fields = ['name']

    def get_queryset(self):
        queryset = super(GroupViewset, self).get_queryset()
        queryset = queryset.order_by('id')
        return queryset

class UserGroupsViewset(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    """
    retrieve:
    返回指定用户的所有角色

    update:
    修改当前用户的角色
    """
    queryset = UserProfile.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        user_obj = self.get_object()
        queryset = user_obj.groups.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return OpsResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        gids = request.data.get("gid", [])
        user_obj.groups = Group.objects.filter(id__in=gids)
        return OpsResponse(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = super(UserGroupsViewset, self).get_queryset()
        return queryset.order_by("id")


class GroupMembersViewset(viewsets.GenericViewSet):
    """
    retrieve: 返回指定组的成员列表
    update: 往指定组里添加成员
    destroy: 从指定组里删除成员
    """
    serializer_class = GroupMembersSerizlizer
    queryset = Group.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        queryset = self.filter_queryset(instance.user_set.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserInfoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserInfoListSerializer(queryset, many=True)
        return OpsResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.user_set.add(*serializer.data["uids"])
        return OpsResponse(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.user_set.remove(*serializer.data["uids"])
        return OpsResponse(status=status.HTTP_204_NO_CONTENT)


class GroupPermissionViewset(viewsets.GenericViewSet):
    """
    retrieve: 返回指定组的权限列表
    update: 向指定组里添加权限
    partial_update: 向指定组里添加权限
    destroy: 从指定组里删除权限
    """
    queryset = Group.objects.all()
    serializer_class = GroupPermissionSerizlizer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        queryset = self.filter_queryset(instance.pms_group.all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PmsPermissionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PmsPermissionSerializer(queryset, many=True)
        return OpsResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.pms_group.add(*serializer.data["pids"])
        return OpsResponse(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.pms_group.remove(*serializer.data["pids"])
        return OpsResponse(status=status.HTTP_204_NO_CONTENT)
