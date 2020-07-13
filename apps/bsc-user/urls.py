#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from apps.user import views


urlpatterns = [
    # 用户
    path("jwt-token", obtain_jwt_token),
    path("user/info", views.UserInfo.as_view(), name="user-info"),
    path("user/testApi", views.TestApiPermission.as_view(), name="user-test-api"),
]
