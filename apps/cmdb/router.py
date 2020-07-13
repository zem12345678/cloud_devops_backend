from .views import dict,scan,asset,connection,business,group,label
from rest_framework import routers
from django.urls import path
from .views import dict,scan,asset,table
cmdb_router = routers.DefaultRouter()
cmdb_router.register(r'dicts', dict.DictViewSet, base_name="dicts")
cmdb_router.register(r'scan/devices', scan.DeviceScanInfoViewSet, base_name="scan_devices")
cmdb_router.register(r'devices', asset.DeviceInfoViewSet, base_name="devices")
cmdb_router.register(r'connections', connection.ConnectionInfoViewSet, base_name="connections")
cmdb_router.register(r'businesses', business.BusinessViewSet, base_name="businesses")
cmdb_router.register(r'groups', group.DeviceGroupViewSet, base_name="groups")
cmdb_router.register(r'labels', label.LabelViewSet, base_name="labels")
