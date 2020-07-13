# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm
from rest_framework.viewsets import ModelViewSet
from ..models import Permission
from ..serializers.permission_serializer import PermissionListSerializer
from commons.custom import CommonPagination, RbacPermission, TreeAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


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
