from rest_framework.routers import DefaultRouter
from .views import ListKeyView, AddKeyView, AclViewSet, SlsViewSet, MdlViewSet, ArgViewSet, MinonStatusViewSet, RejectKeyView, DeleteKeyView, JobsHistoryView, \
    JobsActiveView, JobsKillView, JobsScheduleView, JobsDetailView, GrainsView, PillarView, ExecuteView, \
    CmdHistoryViewSet
from django.conf.urls import include, url

salt_router = DefaultRouter()
salt_router.register(r'minion/status', MinonStatusViewSet, base_name="minion_status")
salt_router.register(r'acl', AclViewSet, base_name="salt_acl")
salt_router.register(r'sls', SlsViewSet, base_name="salt_sls")
salt_router.register(r'mdl', MdlViewSet, base_name="salt_mdl")
salt_router.register(r'arg', ArgViewSet, base_name="salt_arg")
salt_router.register(r'history', CmdHistoryViewSet, base_name="salt_history")

urlpatterns = [
    url(r'^', include(salt_router.urls)),
    # key管理
    url(r'^key/$', ListKeyView.as_view(), name='key_list'),
    url(r'^key/add/$', AddKeyView.as_view(), name='key_add'),
    url(r'^key/reject/$', RejectKeyView.as_view(), name='key_reject'),
    url(r'^key/delete/$', DeleteKeyView.as_view(), name='key_delete'),

    # Job管理
    url(r'^jobs/history/$', JobsHistoryView.as_view(), name="jobs_history"),
    url(r'^jobs/active/$', JobsActiveView.as_view(), name="jobs_active"),
    url(r'^jobs/detail/$', JobsDetailView.as_view(), name="jobs_detail"),
    url(r'^jobs/kill/$', JobsKillView.as_view(), name="jobs_kill"),
    url(r'^jobs/schedule/$', JobsScheduleView.as_view(), name="jobs_schedule"),

    # 数据管理
    url(r'^minion/grains/$', GrainsView.as_view(), name="salt_grains"),
    url(r'^minion/pillar/$', PillarView.as_view(), name="salt_pillar"),

    # 执行
    url(r'^execute/$', ExecuteView.as_view(), name="salt_execute"),
]
