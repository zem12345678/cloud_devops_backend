#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

from django.urls import path
from servicetree import views


urlpatterns = [
    # 分类管理
    path("service-tree", views.ServiceTree.as_view(), name="service-tree"),
    path("bind-cmdb", views.BindCMDBData.as_view(), name="bind-cmdb"),
    path("service-tree-cmdb", views.ServiceTreeCMDB.as_view(), name="service-tree-cmdb"),
    path("service-tree-cmdb-table", views.ServiceTreeCMDBTable.as_view(), name="service-tree-cmdb-table"),
    path("service-tree-not-cmdb", views.ServiceTreeNotCMDB.as_view(), name="service-tree-not-cmdb"),
]
