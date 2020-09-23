from rest_framework import viewsets,mixins,permissions
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from .models import Manufacturer, ProductModel,Idc, Cabinet, Product, Server, NetworkDevice, IP
from .serializers import ManufacturerSerializer, ProductModelSerializer, IdcSerializer, CabinetSerializer,\
    ProductSerializer,ServerSerializer, NetworkDeviceSerializer, IPSerializer, AutoReportSerializer
from .filter import ManufacturerFilter, ProductModelFilter,IdcFilter,CabinetFilter,ProductFilter,ServerFilter,\
    NetworkDeviceFilter, IpFilter
from cloud_devops_backend.code import *
from cloud_devops_backend.basic import OpsResponse

class ManufacturerViewset(CacheResponseMixin,viewsets.ModelViewSet):
    """
    retrieve:
    返回指定制造商信息

    list:
    返回制造商列表

    update:
    更新制造商信息

    destroy:
    删除制造商记录

    create:
    创建制造商资源

    partial_update:
    更新部分字段

    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filter_class = ManufacturerFilter
    filter_fields = ("vendor_name",)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        instance = self.get_object()

        if ProductModel.objects.filter(vendor_id__exact=instance.id).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "该制造商还有产品型号记录，不能删除"
            return OpsResponse(ret, status=BAD)

        self.perform_destroy(instance)
        return OpsResponse(ret, status=OK)

class ProductModelViewset(CacheResponseMixin,viewsets.ModelViewSet):
    """
    retrieve:
    返回指定产品型号信息

    list:
    返回产品型号列表

    update:
    更新产品型号信息

    destroy:
    删除产品型号记录

    create:
    创建产品型号资源

    partial_update:
    更新部分字段
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    filter_class = ProductModelFilter
    filter_fields = ("model_name",)

class IdcViewset(CacheResponseMixin,viewsets.ModelViewSet):
    """
    list:
    返回idc列表

    create:
    创建idc记录

    retrieve:
    返回idc记录

    destroy
    删除idc记录

    update:
    更新idc记录
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    filter_class = IdcFilter
    filter_fields = ("name",)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        instance = self.get_object()

        if Cabinet.objects.filter(idc_id__exact=instance.id).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "该IDC还有机房记录，不能删除"
            return OpsResponse(ret, status=BAD)

        self.perform_destroy(instance)
        return OpsResponse(ret, status=OK)

class CabinetViewset(CacheResponseMixin,viewsets.ModelViewSet):
    """
    list:
    返回机柜列表

    create:
    创建机柜记录

    retrieve:
    返回机柜记录

    destroy
    删除机柜记录

    update:
    更新机柜记录
    """
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    filter_class = CabinetFilter
    filter_fields = ("name", "idc")

class ProductViewset(CacheResponseMixin,viewsets.ModelViewSet):
    """
    retrieve:
    返回指定业务线信息

    list:
    返回业务线列表

    update:
    更新业务线信息

    destroy:
    删除业务线记录

    create:
    创建业务线资源

    partial_update:
    更新部分字段
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    extra_perms_map = {
        "GET": ["products.view_product"]
    }
    filter_class = ProductFilter
    filter_fields = ("pid",)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        instance = self.get_object()
        if instance.pid == 0:
            # 顶级业务线
            # 查找二级级业务线
            if Product.objects.filter(pid__exact=instance.id).count() != 0:
                ret["status"] = 1
                ret["errmsg"] = "该业务下还有二级业务线"
                return OpsResponse(ret, status=BAD)
        else:
            # 二级业务线
            if Server.objects.filter(server_purpose__id__exact=instance.id).count() != 0:
                ret["status"] = 1
                ret["errmsg"] = "该分组下还有产品线，不能删除"
                return OpsResponse(ret, status=BAD)

        self.perform_destroy(instance)
        return OpsResponse(ret, status=status.HTTP_200_OK)

class ProductManageViewSet(CacheResponseMixin,mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    list:
    业务线管理
    """
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        data = self.get_products()
        return OpsResponse(data)

    def get_products(self):
        ret = []
        for obj in self.queryset.filter(pid=0):
            node = self.get_node(obj)
            node["children"] = self.get_children(obj.id)
            ret.append(node)
        return ret

    def get_children(self, pid):
        ret = []
        for obj in self.queryset.filter(pid=pid):
            ret.append(self.get_node(obj))
        return ret

    def get_node(self, product_obj):
        node = {}
        node["id"] = product_obj.id
        node["label"] = product_obj.service_name
        node["pid"] = product_obj.pid
        return node

class ServerViewset(CacheResponseMixin,viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin):
    """
    list:
    获取服务器列表

    create:
    创建服务器

    retrieve:
    获取指定服务器记录

    update:
    修改服务器记录
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    #extra_perms_map = {
    #    "GET": ["products.view_product"]
    #}
    filter_class = ServerFilter
    filter_fields = ('hostname', 'idc', 'cabinet', "service", "server_purpose", "server_type")

    def get_queryset(self):
        queryset = super(ServerViewset, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset

class NetwokDeviceViewset(CacheResponseMixin,viewsets.ReadOnlyModelViewSet):
    """
    list:
    获取网卡列表

    retrieve:
    获取指定网卡记录

    """
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    filter_class = NetworkDeviceFilter
    filter_fields = ("name",)

class IPViewset(CacheResponseMixin,viewsets.ReadOnlyModelViewSet):
    """
    list:
    获取网卡IP列表


    retrieve:
    获取指定网卡IP记录
    """
    queryset = IP.objects.all()
    serializer_class = IPSerializer
    filter_class = IpFilter
    filter_fields = ("ip_addr",)

class ServerAutoReportViewset(CacheResponseMixin,mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """
    agent采集的信息入库
    """
    queryset = Server.objects.all()
    serializer_class = AutoReportSerializer
    permission_classes = (permissions.AllowAny,)

class ServerCountViewset(CacheResponseMixin,viewsets.ViewSet,mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Server.objects.all()

    def list(self, request, *args, **kwargs):
        data = self.get_server_nums()
        return OpsResponse(data)

    def get_server_nums(self):
        ret = {
            "count": self.queryset.count(),
            "vm_host_num": self.queryset.filter(server_type__exact=0).count(),
            "phy_host_num": self.queryset.filter(server_type__exact=1).count(),
            "master_host_num": self.queryset.filter(server_type__exact=2).count()
        }
        return ret