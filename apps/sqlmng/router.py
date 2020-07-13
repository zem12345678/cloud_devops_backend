from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import *

# register的可选参数 base_name: 用来生成urls名字，如果viewset中没有包含queryset, base_name一定要有

sqlmng_router = DefaultRouter()
sqlmng_router.register(r'dbconfs', DbViewSet)
sqlmng_router.register(r'inceptions', InceptionMainView, base_name='Inceptionmainview')
sqlmng_router.register(r'inceptioncheck', InceptionCheckView, base_name='Inceptioncheckview')