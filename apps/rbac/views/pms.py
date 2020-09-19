# @Time    : 2020/9/19 19:29
# @Author  : ZhangEnmin
# @FileName: pms.py
# @Software: PyCharm
from rest_framework import viewsets, mixins,status
from ..models import PerAppName, NodeInfo, PmsPermission
from ..serializers.pms_serializer import PerAppNameSerializer, NodeInfoSerializer, AuthPerSerializer, PmsPermissionSerializer
from rest_framework.pagination import PageNumberPagination
from ..filters import PerAppNameFilter, NodeinfoFilter, PmsPermissionFilter
from cloud_devops_backend.basic import OpsResponse

class PerAppNameViewSet(viewsets.ModelViewSet):
    """
    create:
        创建app名称和UUID
    """
    queryset = PerAppName.objects.all()
    serializer_class = PerAppNameSerializer
    filter_class = PerAppNameFilter
    filter_fields = ("app_name")


class AuthPerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    create:
    权限验证
    """
    queryset = PerAppName.objects.all()
    serializer_class = AuthPerSerializer

    def create(self, request, *args, **kwargs):
        app_key = request.POST.get('app_key', None)
        app_name = request.POST.get('app_name', None)
        try:
            per_obj = PerAppName.objects.get(app_key=app_key)
            if app_name == per_obj.app_name:
                ret = {
                    "status": 1,
                    "app_name": per_obj.app_name,
                    "msg": '授权成功'
                }
                return OpsResponse(ret)
            else:
                return OpsResponse({"status": 0, "app_name": per_obj.app_name, "msg": "权限验证失败"})
        except PerAppName.DoesNotExist:
            return OpsResponse({"status": 0, "msg": "授权失败"})

class NodeInfoViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    返回指定Node信息
    list:
    返回Node列表
    update:
    更新Node信息
    destroy:
    删除Node记录
    create:
    创建Node资源
    partial_update:
    更新部分字段
    """
    queryset = NodeInfo.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NodeInfoSerializer
    filter_class = NodeinfoFilter
    filter_fields = ("node_name")

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        instance = self.get_object()
        print(instance)
        if instance.pid == 0:
            # 顶级菜单
            # 如果不是顶级菜单查找instance.id是否在所有对象pid里面
            if NodeInfo.objects.filter(pid__exact=instance.id).count() != 0:
                ret["status"] = 1
                ret["errmsg"] = "该业务下还有二级业务线"
                return OpsResponse(ret, status=status.HTTP_200_OK)

        self.perform_destroy(instance)
        return OpsResponse(ret, status=status.HTTP_200_OK)

class NodeInfoManageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Nodeinfo信息展示
    """
    pagination_class = PageNumberPagination
    queryset = NodeInfo.objects.all()

    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        data = self.get_nodeinfo()
        return OpsResponse(data)

    def get_nodeinfo(self):
        ret = []

        for obj in self.queryset.filter(pid=0):
            # print(obj.id, obj.node_name)
            node = self.get_node(obj)
            node["children"] = self.get_children(obj.id)
            ret.append(node)
        return ret

    def get_children(self, pid):
        ret = []
        nodes = NodeInfo.objects.filter(pid=pid)
        if len(nodes) == 0:
            return ret

        for child in NodeInfo.objects.filter(pid=pid):
            node = self.get_node(child)
            ret.append(node)
            children = self.get_children(child.id)
            if children:  # 如果存在子节点则加入列表
                node["children"] = children
            elif len(children) == 0:
                del node["children"]  # 删除node字典中children字段
        return ret

    def get_node(self, product_obj):
        node = {}
        node["id"] = product_obj.id
        node["label"] = product_obj.node_name
        node["pid"] = product_obj.pid
        node["path_node"] = product_obj.path_node
        node["children"] = []
        return node

class PmsPermissionViewSet(viewsets.ModelViewSet):
    """
    权限列表 试图类
    list:
    返回权限列表
    update:
    更新权限信息
    destroy:
    删除权限记录
    create:
    创建权限资源
    partial_update:
    更新部分字段
    """
    queryset = PmsPermission.objects.all()
    serializer_class = PmsPermissionSerializer
    filter_class = PmsPermissionFilter
    filter_fields = ("codename")

    def get_queryset(self):
        queryset = super(PmsPermissionViewSet, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset