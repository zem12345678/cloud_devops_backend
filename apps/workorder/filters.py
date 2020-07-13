import django_filters

from django.contrib.auth import get_user_model
from.models import WorkOrder


User = get_user_model()


class WorkOrderFilter(django_filters.rest_framework.FilterSet):
    """
    工单过滤类
    """
    class Meta:
        model = WorkOrder
        fields = ['title']


