# Generated by Django 2.2 on 2020-04-15 18:40

import apps.ticket.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicTicketTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_title', models.CharField(max_length=100, verbose_name='一级标题')),
                ('t_title', models.CharField(max_length=100, verbose_name='二级标题')),
                ('content', models.TextField(blank=True, max_length=1000, null=True, verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('examine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_create_user', to=settings.AUTH_USER_MODEL, verbose_name='工单审核人(默认为工单Leader)')),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_executor', to=settings.AUTH_USER_MODEL, verbose_name='工单执行人(默认为工单部门的OP)')),
            ],
            options={
                'verbose_name': '工单模板',
                'verbose_name_plural': '工单模板',
                'db_table': 'ticket_template',
            },
        ),
        migrations.CreateModel(
            name='TicketDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=100, verbose_name='标题')),
                ('content', django_mysql.models.JSONField(default=apps.ticket.models.JSONFieldDefault)),
                ('status', models.IntegerField(choices=[(0, '申请'), (1, '处理中'), (2, '拒绝'), (3, '完成')], default=0, verbose_name='工单状态')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_creator', to=settings.AUTH_USER_MODEL, verbose_name='工单申请人')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='template_id', to='ticket.BasicTicketTemplate', verbose_name='模板ID')),
            ],
            options={
                'verbose_name': '工单详情',
                'verbose_name_plural': '工单详情',
                'db_table': 'ticket_detail',
            },
        ),
    ]
