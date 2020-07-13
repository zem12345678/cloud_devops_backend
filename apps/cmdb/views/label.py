# @Time    : 2020/4/24 22:34
# @Author  : ZhangEnmin
from rest_framework.viewsets import ModelViewSet
from ..models import Label
from ..serializers.label_serializer import LabelSerializer
from commons.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication

class LabelViewSet(ModelViewSet):
    '''
    标签管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'lebel_all'}, {'get': 'lebel_list'}, {'post': 'lebel_create'}, {'put': 'lebel_edit'},
                 {'delete': 'lebel_delete'}, {'patch': 'lebel_edit'}, {'get': 'device_list'})
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,TokenAuthentication,SessionAuthentication,BasicAuthentication,)
    permission_classes = (RbacPermission,)