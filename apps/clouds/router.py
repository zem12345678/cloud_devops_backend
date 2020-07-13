from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewset, CloudInstanceViewset


clouds_router = DefaultRouter()
clouds_router.register(r'clouds/manufacturer', ManufacturerViewset, base_name="manufacturer")
clouds_router.register(r'clouds/instance', CloudInstanceViewset, base_name="instance")