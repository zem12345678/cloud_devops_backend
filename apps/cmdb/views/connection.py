# @Time    : 2020/7/12
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm/24 20:38
# @Author  : ZhangEnmin
from rest_framework.viewsets import ModelViewSet
from ..serializers.connection_serializer import ConnectionInfoSerializer
from commons.custom import CommonPagination, RbacPermission, ObjPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from ..models import ConnectionInfo
from cloud_devops_backend.basic import OpsResponse
from cloud_devops_backend.code import *
from django.db.models import Q

class ConnectionInfoViewSet(ModelViewSet):
    '''
    连接信息管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'connection_all'}, {'get': 'connection_list'}, {'post': 'connection_create'}, {'put': 'connection_edit'},
                 {'delete': 'connection_delete'})
    queryset = ConnectionInfo.objects.all()
    serializer_class = ConnectionInfoSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('hostname',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,TokenAuthentication,SessionAuthentication,BasicAuthentication,)
    permission_classes = (RbacPermission,ObjPermission)

    def create(self, request, *args, **kwargs):
        # 创建密码时自动绑定uid
        request.data['uid'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return OpsResponse(serializer.data, status=CREATED, headers=headers)

    def get_queryset(self):
        '''
        当前用户只能看到自己创建和已公开的密码
        '''
        perms = RbacPermission.get_permission_from_role(self.request)
        if 'admin' in perms:
            return self.queryset.all()
        else:
            return self.queryset.filter(Q(uid_id=self.request.user.id) | Q(is_public=True))