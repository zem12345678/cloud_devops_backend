import django.utils.timezone as timezone
from django.db import models
from rbac.models import Organization


class ServiceTree(models.Model):
    """ 服务树 """
    label = models.CharField(verbose_name="名称", max_length=128)
    parent = models.IntegerField(verbose_name="父亲级别")
    level = models.IntegerField(verbose_name="层级")
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'service_tree'
        verbose_name = "服务树"
        verbose_name_plural = "服务树"
        app_label = 'servicetree'

class BindCMDB(models.Model):
    """ 服务树绑定的CMDB数据 """
    service_tree = models.IntegerField(verbose_name="服务树ID")
    classification = models.IntegerField(verbose_name="分类ID")
    table = models.IntegerField(verbose_name="表ID")
    data = models.IntegerField(verbose_name="数据ID")

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'service_tree_cmdb'
        verbose_name = "服务树绑定CMDB"
        verbose_name_plural = "服务树绑定CMDB"
        index_together = ["service_tree", "classification", "table"]
        app_label = 'servicetree'


class Node(models.Model):
    "组织树"
    name = models.CharField("节点名称", max_length=32, db_index=True, help_text="service名称")
    pid = models.IntegerField("节点pid", db_index=True, help_text="pid")
    path = models.CharField("节点中文path", max_length=32, db_index=True, help_text="node中文path")
    rd = models.CharField("业务负责人", max_length=255, null=True, blank=True, help_text="业务负责人")
    op = models.CharField("运维负责人", max_length=255, null=True, blank=True, help_text="运维负责人")
    groups = models.ManyToManyField(Organization, verbose_name="用户组关联节点", related_name="node_group",
                                    help_text="用户组关联节点")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "servicetree_node"
        ordering = ["id"]
        app_label = 'servicetree'
