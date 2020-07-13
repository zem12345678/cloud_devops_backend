#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

from django.urls import path
from apps.task import views


urlpatterns = [
    # 分类管理
    path("task-list", views.TaskList.as_view(), name="task-list"),
    path("execute-task", views.ExecuteTask.as_view(), name="execute-task"),
    path("scheduled-task", views.ScheduledTask.as_view(), name="scheduled-task"),
    path("task-history", views.TaskHistory.as_view(), name="task-history"),
    path("task-history-details", views.TaskHistoryDetails.as_view(), name="task-history-details"),
]
