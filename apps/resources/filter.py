import django_filters

from .models import Manufacturer, ProductModel,Idc,Cabinet,Product,Server,IP,NetworkDevice
from django.db.models import Q

class ManufacturerFilter(django_filters.rest_framework.FilterSet):
    """
    制造商滤类
    """
    vendor_name = django_filters.CharFilter(field_name="vendor_name", lookup_expr="icontains")

    class Meta:
        model  = Manufacturer
        fields = ['vendor_name']

class ProductModelFilter(django_filters.rest_framework.FilterSet):
    """
    机器型号过滤类
    """
    model_name = django_filters.CharFilter(field_name="model_name", lookup_expr="icontains")


    class Meta:
        model  = ProductModel
        fields = ['model_name']

class IdcFilter(django_filters.rest_framework.FilterSet):
    """
    IDC机房过滤类
    """
    name = django_filters.CharFilter(method='search_idc')

    def search_idc(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value)|Q(letter__icontains=value))


    class Meta:
        model = Idc
        fields = ['name']

class CabinetFilter(django_filters.rest_framework.FilterSet):
    """
    机柜过滤类
    """
    name = django_filters.CharFilter(lookup_expr="icontains")
    idc = django_filters.NumberFilter(method="search_idc")

    def search_idc(self, queryset, name, value):
        return queryset.filter(idc__pk=value)


    class Meta:
        model  = Cabinet
        fields = ['name', 'idc']


class ProductFilter(django_filters.rest_framework.FilterSet):
    """
    业务线过滤类
    """
    pid     = django_filters.NumberFilter(field_name="pid")


    class Meta:
        model = Product
        fields = ['pid']

class ServerFilter(django_filters.rest_framework.FilterSet):
    """
    服务器过滤类
    """

    hostname        = django_filters.CharFilter(method='search_server')
    idc             = django_filters.NumberFilter(method="search_idc")
    cabinet         = django_filters.NumberFilter(method="search_cabinet")
    service         = django_filters.NumberFilter(method="search_first_product")
    server_purpose  = django_filters.NumberFilter(method="search_second_product")
    server_type     = django_filters.ChoiceFilter(field_name="server_type", choices=((0,"vm"), (1, "物理机"),(2, "宿主机")), lookup_expr="exact")


    def search_server_type(self,queryset, name, value):
        if value == 0:
            return queryset.filter(server_type__in=[0,1])
        else:
            return queryset.filter(server_type=value)


    def search_second_product(self, queryset, name, value):
        if value > 0:
            return queryset.filter(server_purpose_id__exact=value)
        elif value == -1:
            return queryset.filter(server_purpose_id__isnull=True)
        else:
            return queryset

    def search_first_product(self, queryset, name, value):
        if value > 0:
            return queryset.filter(service_id__exact=value)
        elif value == -1:
            return queryset.filter(service_id__isnull=True)
        else:
            return queryset

    def search_server(self, queryset, name, value):
        return queryset.filter(Q(hostname__icontains=value)|Q(manage_ip__icontains=value))


    def search_idc(self, queryset, name, value):
        if value > 0:
            return queryset.filter(idc_id__exact=value)
        elif value == -1:
            return queryset.filter(idc_id__isnull=True)
        else:
            return queryset

    def search_cabinet(self, queryset, name, value):
        if value > 0:
            return queryset.filter(cabinet_id__exact=value)
        elif value == -1:
            return queryset.filter(cabinet_id__isnull=True)
        else:
            return queryset

    class Meta:
        model = Server
        fields = ['hostname', 'idc', 'cabinet', "service_id", "server_purpose","server_type"]


class NetworkDeviceFilter(django_filters.rest_framework.FilterSet):
    """
    网卡过滤类
    """
    name = django_filters.CharFilter(method='search_name')

    def search_name(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))


    class Meta:
        model  = NetworkDevice
        fields = ['name']


class IpFilter(django_filters.rest_framework.FilterSet):
    """
    网卡过滤类
    """
    ip_addr = django_filters.CharFilter(method='search_ip')

    def search_ip(self, queryset, ip_addr, value):
        return queryset.filter(Q(ip_addr__icontains=value))


    class Meta:
        model  = IP
        fields = ['ip_addr']