from rest_framework.routers import DefaultRouter
from .views import PerAppNameViewSet, AuthPerViewSet, PermissionViewSet

pms_router = DefaultRouter()
# pms_router.register("pms/perappname", PerAppNameViewSet, base_name='perappname')
# pms_router.register("pms/authper", AuthPerViewSet, base_name='authper')
pms_router.register("pms/permission", PermissionViewSet, base_name='permission')
