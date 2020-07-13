from rest_framework.routers import DefaultRouter
from servicetree.views import ServiceTreeViewSet, NodeViewSet

servicetree_router = DefaultRouter()
servicetree_router.register("servicetree/node", NodeViewSet, base_name='node')
servicetree_router.register("servicetree", ServiceTreeViewSet, base_name='nodemanage')
