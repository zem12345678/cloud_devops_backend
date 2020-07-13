# -*- coding:utf8 -*-

import django_filters
from .models import Account, Permisssion,Auditor


class AccountFilter(django_filters.FilterSet):
    """
    Server filter.
    """
    class Meta:
        model = Account
        fields = {
            "username": ['exact'],
        }


class PermissionFilter(django_filters.FilterSet):
    class Meta:
        model = Permisssion
        fields = {
            "username": ['exact'],
            "hostname": ["exact"]
        }


class AuditorFilter(django_filters.FilterSet):
    class Meta:
        model = Auditor
        fields = {
            "login_user":['exact'],
            "local_ip":['exact'],
            "exec_user":['exact'],
            "exec_time":['gt','lt'],
            "command_info":['icontains']
        }
