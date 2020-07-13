import django_filters
from .models import Organization

class OrgFilter(django_filters.FilterSet):
    '''
    Group 搜索类
    '''
    name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤用户组')

    class Meta:
        model = Organization
        fields = ['name']


