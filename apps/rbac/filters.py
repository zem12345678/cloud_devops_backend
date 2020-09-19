import django_filters
from django.contrib.auth.models import Permission
from django.db.models import Q
from .models import UserProfile,PerAppName,PmsPermission,NodeInfo
from django.contrib.auth.models import Group

class AuthPermissionFilter(django_filters.rest_framework.FilterSet):
    """
    权限过滤类
    """
    name = django_filters.CharFilter(method='search_permission')
    def search_permission(self, queryset, name, value):
        return queryset.filter(Q(codename__icontains=value)|
                               Q(content_type__app_label__icontains=value)|
                               Q(content_type__model__icontains=value))

    class Meta:
        model = Permission
        fields = ['name']

class UserFilter(django_filters.rest_framework.FilterSet):
    """
    用户过滤类
    """
    username = django_filters.CharFilter(method='search_username')

    def search_username(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(username__icontains=value))

    class Meta:
        model = UserProfile
        fields = ['username']

class PerAppNameFilter(django_filters.FilterSet):
    """
    AppName 搜索类
    """
    app_name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤app名称')

    class Meta:
        model = PerAppName
        fields = ['app_name']

class PmsPermissionFilter(django_filters.FilterSet):
    """
    Permission 搜索类
    """
    codename = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤权限名称')

    class Meta:
        model = PmsPermission
        fields = ['codename']

class NodeinfoFilter(django_filters.FilterSet):
    '''
    NodeName 搜索类
    '''
    node_name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤node节点名称')

    class Meta:
        model = NodeInfo
        fields = ['node_name']

class GroupFilter(django_filters.rest_framework.FilterSet):
    '''
    Group 搜索类
    '''
    name = django_filters.CharFilter(name='name',lookup_expr='icontains', help_text='过滤用户组')

    class Meta:
        model = Group
        fields = ['name']
