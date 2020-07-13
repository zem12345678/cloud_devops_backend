from rest_framework.routers import DefaultRouter
from .views import TasksViewset

task_router = DefaultRouter()
task_router.register(r'task', TasksViewset, base_name="task")

