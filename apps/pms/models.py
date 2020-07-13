from django.db import models
from django.contrib.auth.models import Group
from orgs.models import Organization

class PerAppName(models.Model):
    app_key = models.CharField("APPkey", max_length=64, null=False, unique=True, help_text="APPkey")
    app_name = models.CharField("APP名称", max_length=32, null=False, blank=False, help_text="APP名称")
    app_desc = models.CharField("APP应用描述", max_length=32, blank=False, help_text="APP应用描述")

    def __str__(self):
        return self.app_name

    class Meta:
        db_table = "pms_app"


class Permission(models.Model):
    codename = models.CharField("权限简称", max_length=64, help_text="权限简称")
    desc = models.CharField("权限描述信息", max_length=64, help_text="权限描述信息")
    app = models.CharField("APP名称", max_length=64, help_text="APP名称")
    groups = models.ManyToManyField(Organization, verbose_name="用户组关联权限", related_name="pms_group", help_text="用户组关联权限")

    def __str__(self):
        return self.codename

    class Meta:
        db_table = 'pms_permission'
        ordering = ['id']
