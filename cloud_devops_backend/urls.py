"""cloud_devops_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include
from django.conf.urls.static import serve

from cloud_devops_backend.settings import MEDIA_ROOT
from cloud_devops_backend.settings import STATIC_ROOT

from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
import xadmin


from book.router import books_router
from cmdb.router import cmdb_router
from zabbix.router import zabbix_router
from workorder.router import workorder_router
from sqlmng.router import sqlmng_router
from resources.router import resources_router
from clouds.router import clouds_router
from release.router import deploy_router
from servicetree.router import servicetree_router
from autotask.router import task_router

schema_view = get_schema_view(title='API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
router = DefaultRouter()


router.registry.extend(books_router.registry)
router.registry.extend(cmdb_router.registry)
router.registry.extend(zabbix_router.registry)
router.registry.extend(workorder_router.registry)
router.registry.extend(sqlmng_router.registry)
router.registry.extend(resources_router.registry)
router.registry.extend(clouds_router.registry)
router.registry.extend(deploy_router.registry)
router.registry.extend(task_router.registry)
router.registry.extend(servicetree_router.registry)

urlpatterns = [
    # path(r'', include('cmdb.urls')),
    path(r'', include('deployment.urls')),
    path(r'', include('rbac.urls')),
    path(r'', include('servicetree.urls')),
    path(r'', include(router.urls)),
    path(r'salt/', include('salt.urls')),
    # path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    path(r'admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'jwt-refresh/', refresh_jwt_token),
    path(r'swagger-docs/', schema_view, name='swagger-docs'),
    path(r'docs/', include_docs_urls("开源自动化运维云管理平台")),
    re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT }),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),


]
