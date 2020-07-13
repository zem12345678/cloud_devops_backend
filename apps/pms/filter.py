import django_filters
from pms.models import PerAppName, Permission


class PerAppNameFilter(django_filters.FilterSet):
    """
    AppName 搜索类
    """
    app_name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤app名称')

    class Meta:
        model = PerAppName
        fields = ['app_name']


class PermissionFilter(django_filters.FilterSet):
    """
    Permission 搜索类
    """
    codename = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤权限名称')

    class Meta:
        model = Permission
        fields = ['codename']
