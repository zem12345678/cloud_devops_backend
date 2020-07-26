from rest_framework.routers import DefaultRouter
from .views import K8sNodeListView,K8sPodListView,K8sServiceListView,K8sPodWebSsh

k8s_router = DefaultRouter()
k8s_router.register(r'k8sNode', K8sNodeListView, base_name="k8sNode")
k8s_router.register(r'k8sPod', K8sPodListView, base_name="k8sPod")
k8s_router.register(r'k8sPodWebSsh', K8sServiceListView, base_name="k8sPodWebSsh")
k8s_router.register(r'k8sPodWebSsh', K8sPodWebSsh, base_name="k8sPodWebSsh")