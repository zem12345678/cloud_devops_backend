from rest_framework import viewsets, response
from .models import PerAppName, Permission
from .serializers import PerAppNameSerializer, AuthPerSerializer, PermissionSerializer
from .filter import PerAppNameFilter, PermissionFilter


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
                return response.Response(ret)
            else:
                return response.Response({"status": 0, "app_name": per_obj.app_name, "msg": "权限验证失败"})
        except PerAppName.DoesNotExist:
            return response.Response({"status": 0, "msg": "授权失败"})


class PermissionViewSet(viewsets.ModelViewSet):
    """
    list:
    获取权限列表
    update:
    更新权限信息
    destroy:
    删除权限信息
    create:
    创建权限
    partial_update:
    更新权限信息
    retrieve:
    获取权限信息
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilter
    filter_fields = ("codename")

    def get_queryset(self):
        queryset = super(PermissionViewSet, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset
