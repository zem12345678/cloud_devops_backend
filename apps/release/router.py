from rest_framework.routers import DefaultRouter
from .views import DeployViewset

deploy_router = DefaultRouter()
deploy_router.register(r'deploy', DeployViewset, base_name="deploy")
