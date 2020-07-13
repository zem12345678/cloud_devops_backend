import django_filters
from django.contrib.auth.models import Group

class GroupFilter(django_filters.FilterSet):
    '''
    Group 搜索类
    '''
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤用户组')

    class Meta:
        model = Group
        fields = ['name']


