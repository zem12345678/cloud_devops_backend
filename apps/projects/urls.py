from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^list/$', ProjectListView.as_view(), name='project_list'),
    url('^tag/$',ProjectVersionsView.as_view(), name='project_tag')
]
