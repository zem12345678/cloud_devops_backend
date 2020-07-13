import coreapi
import django_filters
from .models import SaltArg, SaltMdl, SaltSls, SaltAcl, MinionsStatus, CmdHistory
from rest_framework import filters
from rest_framework.schemas import AutoSchema


class MinionStatusFilter(django_filters.FilterSet):
    """
    搜索状态文件名称
    """
    minion_id = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤主机名称')
    minion_status = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤主机状态')

    class Meta:
        model = MinionsStatus
        fields = '__all__'


class SaltSlsFilter(django_filters.FilterSet):
    """
    搜索状态文件名称
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤状态文件名称')

    class Meta:
        model = SaltSls
        fields = ['name']


class SaltArgFilter(django_filters.FilterSet):
    """
    搜索模块参数
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤参数名称')

    class Meta:
        model = SaltArg
        fields = ['name']


class SaltMdlFilter(django_filters.FilterSet):
    """
    搜索模块名称
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤模块名称')

    class Meta:
        model = SaltMdl
        fields = ['name']


class SaltAclFilter(django_filters.FilterSet):
    """
    搜索模块名称
    """
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤ACL名称')

    class Meta:
        model = SaltAcl
        fields = ['name', 'deny']


class HistoryFilter(django_filters.FilterSet):
    """
    搜索模块名称
    """
    type = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤ACL名称')
    executor = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤执行人')
    command = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤历史命令')

    class Meta:
        model = CmdHistory
        fields = ['type', 'command', 'executor']



# class CustomFilter(filters.BaseFilterBackend):
#
#     def get_schema_fields(self, view):
#         fields = []
#         defaults = dict(
#             location='query', required=False,
#             type='string', example='',
#             description=''
#         )
#
#         if not hasattr(view, 'custom_filter_fields'):
#             return []
#
#         for field in view.custom_filter_fields:
#             if isinstance(field, str):
#                 defaults['name'] = field
#             elif isinstance(field, dict):
#                 defaults.update(field)
#             else:
#                 continue
#             fields.append(coreapi.Field(**defaults))
#         return fields
#
#     def filter_queryset(self, request, queryset, view):
#         return queryset