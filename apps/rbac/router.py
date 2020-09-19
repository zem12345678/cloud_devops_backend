# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm
from rest_framework.routers import DefaultRouter
from .views.permission import AuthPermissionsViewset, GroupPermissionsViewset


permission_router = DefaultRouter()
permission_router.register(r'authPermissions', AuthPermissionsViewset, base_name="authPermissions")
permission_router.register(r'grouppermissions', GroupPermissionsViewset, base_name="grouppermissions")