# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, mixins,status
from ..models import Permission
from ..serializers.permission_serializer import PermissionListSerializer,AuthPermissionSerializer
from commons.custom import CommonPagination, RbacPermission, TreeAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import get_object_or_404
from ..common import get_permission_obj
from django.contrib.auth.models import Permission as AuthPermission, Group
from ..filters import AuthPermissionFilter
from cloud_devops_backend.basic import OpsResponse


class PermissionViewSet(ModelViewSet, TreeAPIView):
    '''
    权限：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'permission_all'}, {'get': 'permission_list'}, {'post': 'permission_create'},
                 {'put': 'permission_edit'},{'delete': 'permission_delete'})
    queryset = Permission.objects.all()
    serializer_class = PermissionListSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)



class PermissionTreeView(TreeAPIView):
    '''
    权限树
    '''
    queryset = Permission.objects.all()



class AuthPermissionsViewset(viewsets.ReadOnlyModelViewSet):
    """
    权限列表 视图类

    list:
    返回permission列表

    """
    queryset = AuthPermission.objects.all()
    serializer_class = AuthPermissionSerializer
    filter_class = AuthPermissionSerializer
    filter_fields = ("name",)

    def get_queryset(self):
        queryset = super(AuthPermissionsViewset, self).get_queryset()
        queryset = queryset.order_by("content_type__id")
        return queryset


class GroupPermissionsViewset(viewsets.ReadOnlyModelViewSet,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin):
    """
    用户组权限

    retrieve:
    返回用户组的权限列表

    update:
    给指定用户组增加权限，参数pid: permission id

    destroy:
    删除指定组下的权限，参数pid: permission id
    """

    queryset = AuthPermission.objects.all()
    serializer_class = AuthPermissionSerializer
    filter_class = AuthPermissionFilter
    filter_fields = ("name",)

    def process_permission(self, group_permission_queryset, data):
        for record in data:
            try:
                group_permission_queryset.get(pk=record.get("id", None))
                record["status"] = True
            except:
                pass
        return data

    def get_group_permissions(self):
        groupobj = self.get_object()
        queryset = groupobj.permissions.all()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return OpsResponse(serializer.data)

    def get_modify_permissions(self):
        groupobj = self.get_object()
        group_permission_queryset = groupobj.permissions.all()
        queryset = AuthPermission.objects.all()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self.process_permission(group_permission_queryset, serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return OpsResponse(self.process_permission(group_permission_queryset, serializer.data))

    def retrieve(self, request, *args, **kwargs):
        modify = request.GET.get("modify", None)
        if modify is not None:
            return self.get_modify_permissions()
        else:
            return self.get_group_permissions()

    def get_object(self):
        queryset = Group.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        ret = {"status": 0}
        groupobj = self.get_object()
        permission_obj = get_permission_obj(request.data.get("pid", ""))
        if permission_obj is None:
            ret["status"] = 1
            ret["errmsg"] = "permission 不存在"
        else:
            groupobj.permissions.add(permission_obj)
        return OpsResponse(ret, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        groupobj = self.get_object()
        permission_obj = get_permission_obj(request.data.get("pid", ""))
        if permission_obj is None:
            ret["status"] = 1
            ret["errmsg"] = "permission 不存在"
        else:
            groupobj.permissions.remove(permission_obj)
        return OpsResponse(ret, status=status.HTTP_200_OK)