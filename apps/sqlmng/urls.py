#coding=utf-8
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views.inception import *
from .views.inception_check import InceptionCheckView
from .views.select_data import SelectDataView
from .views.target_db import DbViewSet, DbWorkOrderViewSet
from .views.workorder_main import InceptionMainView
from .views.auth_rules import AuthRulesViewSet
from .views.suggestion import SuggestionViewSet
from .views.db_cluster import DbClusterViewSet
from .views.settings import \
    SqlSettingsViewSet, \
    StrategyViewSet, \
    PersonalSettingsViewSet, \
    InceptionVariablesViewSet, \
    InceptionConnectionViewSet, \
    MailActionsSettingsViewSet, \
    InceptionBackupView, \
    ConnectionCheckView, \
    ShowDatabasesView


# register的可选参数 base_name: 用来生成urls名字，如果viewset中没有包含queryset, base_name一定要有

sqlmng_router = DefaultRouter()
#router.register(r'dbconfs', DbViewSet)
#router.register(r'inceptions', InceptionMainView, base_name='Inceptionmainview')
#router.register(r'inceptioncheck', InceptionCheckView, base_name='Inceptioncheckview')
#router.register(r'autoselects/', SelectDataView,base_name='selectdataview')
sqlmng_router.register(r'dbconfs', DbViewSet, base_name='DbViewSet')
sqlmng_router.register(r'inceptions', InceptionMainView, base_name='InceptionMainView')
sqlmng_router.register(r'inceptioncheck', InceptionCheckView, base_name='InceptionCheckView')
sqlmng_router.register(r'autoselects', SelectDataView, base_name='SelectDataView')
sqlmng_router.register(r'sqlsettings', SqlSettingsViewSet, base_name='SqlSettingsViewSet')
sqlmng_router.register(r'strategy', StrategyViewSet, base_name='StrategyViewSet')
sqlmng_router.register(r'personalsettings', PersonalSettingsViewSet, base_name='PersonalSettingsViewSet')
sqlmng_router.register(r'authrules', AuthRulesViewSet, base_name='AuthRulesViewSet')
sqlmng_router.register(r'suggestion', SuggestionViewSet, base_name='SuggestionViewSet')
sqlmng_router.register(r'dbcluster', DbClusterViewSet, base_name='DbClusterViewSet')
sqlmng_router.register(r'mailactions', MailActionsSettingsViewSet, base_name='MailActionsSettingsViewSet')
sqlmng_router.register(r'inception/variables', InceptionVariablesViewSet, base_name='InceptionVariablesViewSet')
sqlmng_router.register(r'inception/connection', InceptionConnectionViewSet, base_name='InceptionConnectionViewSet')
sqlmng_router.register(r'dbworkorder', DbWorkOrderViewSet, base_name='DbWorkOrderViewSet')
sqlmng_router.register(r'chart', ChartViewSet)
urlpatterns = [
    url(r'^', include(sqlmng_router.urls)),
    #url(r'^autoselects/', SelectDataView.as_view(), name='selectdataview'),
    url(r'^download/sqlhandle/(?P<pk>\d+).(?P<sfx>\w+)$', SqlFileView.as_view()),
    url(r'^inception/backup/$', InceptionBackupView.as_view()),
    url(r'^inception/conncheck/$', ConnectionCheckView.as_view()),
    url(r'^inception/showdatabases/$', ShowDatabasesView.as_view()),

]
