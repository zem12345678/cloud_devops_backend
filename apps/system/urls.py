#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

from django.urls import path
from apps.system import views


urlpatterns = [
    # 分类管理
    path("register-apply", views.RegisterApply.as_view(), name="register-apply"),
    path("agent-list", views.AgentList.as_view(), name="agent-list"),
    path("ignore-agent", views.IgnoreAgent.as_view(), name="ignore-agent"),
    # path("blacklist/", views.BlackListViews, name="blacklist"),
    # path("agent_list/", views.AgentListViews, name="agent_list"),
    # path("register_agent/", views.RegisterToAgentViews, name="register_agent"),
    # path("delete_black_agent/", views.DeleteBlackAgentViews, name="delete_black_agent"),
    # path("delete_agent/", views.DeleteAgentViews, name="delete_agent"),
]
