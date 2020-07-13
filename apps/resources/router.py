from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewset, ProductModelViewset,IdcViewset,CabinetViewset,ProductViewset,ProductManageViewSet,ServerViewset, NetwokDeviceViewset, IPViewset, ServerAutoReportViewset, ServerCountViewset


resources_router = DefaultRouter()
resources_router.register(r'manufacturer', ManufacturerViewset, base_name="manufacturer")
resources_router.register(r'product_model', ProductModelViewset, base_name="product_model")
resources_router.register(r'idcs', IdcViewset, base_name="idcs")
resources_router.register(r'cabinet', CabinetViewset, base_name="cabinet")
resources_router.register(r'products', ProductViewset, base_name='products')
resources_router.register(r'productmanage', ProductManageViewSet, base_name="productmanage")
resources_router.register(r'servers', ServerViewset, base_name="servers")
resources_router.register(r'network_device', NetwokDeviceViewset, base_name="network_device")
resources_router.register(r'ip', IPViewset, base_name="ip")
resources_router.register(r'ServerAutoReport', ServerAutoReportViewset, base_name="ServerAutoReport")
resources_router.register(r'ServerCount', ServerCountViewset, base_name="ServerCount")