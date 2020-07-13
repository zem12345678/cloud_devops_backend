from django.db import models


class AgentList(models.Model):

    agent_id = models.CharField(verbose_name="AGENT ID", max_length=128)
    ipaddress = models.CharField(verbose_name="IP地址", max_length=256, null=True, blank=True)
    hostname = models.CharField(verbose_name="主机名称", max_length=128, null=True, blank=True)
    apply_time = models.DateTimeField(verbose_name="agent申请时间", blank=True, null=True)
    last_heartbeat = models.DateTimeField(verbose_name="最后一次心跳时间", blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ipaddress

    class Meta:
        db_table = "system_agent_list"
        verbose_name = "Agent列表"
        verbose_name_plural = "Agent列表"


class AgentApprovalList(models.Model):

    agent_id = models.CharField(verbose_name="AGENT ID", max_length=128)
    ipaddress = models.CharField(verbose_name="IP地址", max_length=256, null=True, blank=True)
    hostname = models.CharField(verbose_name="主机名称", max_length=128, null=True, blank=True)
    apply_time = models.DateTimeField(verbose_name="agent申请时间", blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ipaddress

    class Meta:
        db_table = "system_agent_approval"
        verbose_name = "Agent注册审批"
        verbose_name_plural = "Agent注册审批"


class BlackList(models.Model):

    agent_id = models.CharField(verbose_name="AGENT ID", max_length=128)
    ipaddress = models.CharField(verbose_name="IP地址", max_length=256, null=True, blank=True)
    hostname = models.CharField(verbose_name="主机名称", max_length=128, null=True, blank=True)
    apply_time = models.DateTimeField(verbose_name="agent申请时间", blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ipaddress

    class Meta:
        db_table = "system_blacklist"
        verbose_name = "Agent黑名单"
        verbose_name_plural = "Agent黑名单"
