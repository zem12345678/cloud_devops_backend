# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm
from rest_framework.viewsets import ModelViewSet
from ..models import Business
from ..serializers.business_serializer import BusinessSerializer
from commons.custom import CommonPagination, RbacPermission, TreeAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication

class BusinessViewSet(ModelViewSet, TreeAPIView):
    '''
    业务管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'business_all'}, {'get': 'business_list'}, {'post': 'business_create'}, {'put': 'business_edit'},
                 {'delete': 'business_delete'}, {'patch': 'business_edit'}, {'get': 'device_list'})
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,TokenAuthentication,SessionAuthentication,BasicAuthentication,)
    permission_classes = (RbacPermission,)