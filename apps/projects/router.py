from rest_framework.routers import DefaultRouter
from .views import ProjectViewset


project_router = DefaultRouter()
project_router.register(r'project', ProjectViewset, base_name="project")
