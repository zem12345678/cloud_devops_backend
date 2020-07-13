
from django.conf.urls import url
from apps.bastion.views import AccountView,PermissionView,AuditView,GroupView,PermissionRetrieveView,AccountRetrieveView



urlpatterns = [
    url(r'bastion/account/',AccountView.as_view()),
    url(r'bastion/account/retrieve/(?P<username>\w+)/$',AccountRetrieveView.as_view()),
    url(r'bastion/permission/retrieve/(?P<pk>\d+)/$',PermissionRetrieveView.as_view()),
    url(r'bastion/permission/$',PermissionView.as_view()),
    url(r'bastion/audit/$',AuditView.as_view()),
    url(r'bastion/group/$',GroupView.as_view()),
]