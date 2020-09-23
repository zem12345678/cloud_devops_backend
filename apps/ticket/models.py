from django.db import models

# Create your models here.
from utils.basemodels import Basemodel
from rbac.models import UserProfile
from django_mysql.models import JSONField


def JSONFieldDefault():
    return {}


# 配置模板

class BasicTicketTemplate(Basemodel):
    """
    基础信息
    """
    f_title       = models.CharField(max_length=100, verbose_name=u'一级标题')
    t_title       = models.CharField(max_length=100, verbose_name=u'二级标题')
    content     	= models.TextField(max_length=1000, null=True, blank=True, verbose_name=u'描述')
    create_time         = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time         = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    examine		= models.ForeignKey(UserProfile,
                                  on_delete=models.CASCADE,
                                  verbose_name='工单审核人(默认为工单Leader)',
                                  related_name='ticket_create_user')


    executor       	= models.ForeignKey(UserProfile,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE,
                                verbose_name='工单执行人(默认为工单部门的OP)',
                                related_name='ticket_executor')

    def __str__(self):
        return '{} | {}'.format(self.f_title, self.t_title) 

    class Meta:
        db_table = 'ticket_template'
        verbose_name = '工单模板'
        verbose_name_plural = verbose_name


class TicketDetail(Basemodel):

    CHOICE_TASK_STATUS = (
        (0, '申请'),
        (1, '处理中'),
        (2, '拒绝'),
        (3, '完成'),
    )

    name        = 	models.CharField(max_length=100, verbose_name=u'标题')
    creator     =       models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='工单申请人', related_name='ticket_creator')
    template    =	models.ForeignKey(BasicTicketTemplate, on_delete=models.CASCADE, verbose_name='模板ID', related_name='template_id')
    content     = 	JSONField(default=JSONFieldDefault)
    status      =   	models.IntegerField(choices=CHOICE_TASK_STATUS, default=0, verbose_name='工单状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ticket_detail'
        verbose_name = '工单详情'
        verbose_name_plural = verbose_name
