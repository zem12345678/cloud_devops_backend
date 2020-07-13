from django.db import models


class TaskList(models.Model):

    name = models.CharField(verbose_name="任务名称", max_length=128, null=True, blank=True)
    content = models.TextField(verbose_name="任务内容", null=True, blank=True)
    description = models.CharField(verbose_name="任务描述", max_length=1024, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "task_list"
        verbose_name = "任务列表"
        verbose_name_plural = "任务列表"
        app_label = 'task'


class TaskHistory(models.Model):
    agent = models.CharField(verbose_name="任务名称", max_length=128)
    uuid = models.CharField(verbose_name="任务执行唯一ID", max_length=128)
    task_name = models.CharField(verbose_name="任务名称", max_length=128)
    status = models.CharField(verbose_name="任务状态", max_length=128)
    content = models.TextField(verbose_name="任务状态", blank=True, null=True)
    start_time = models.DateTimeField(verbose_name="开始时间", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="结束时间", blank=True, null=True)

    def __str__(self):
        return self.uuid

    class Meta:
        db_table = "task_history"
        verbose_name = "执行历史"
        verbose_name_plural = "执行历史"
        app_label = 'task'
