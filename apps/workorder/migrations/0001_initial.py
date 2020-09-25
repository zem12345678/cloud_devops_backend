# Generated by Django 2.2.14 on 2020-09-25 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='工单标题')),
                ('type', models.IntegerField(choices=[(0, '数据库'), (1, 'WEB服务'), (2, '计划任务'), (3, '配置文件'), (4, '其它')], default=0, verbose_name='工单类型')),
                ('order_contents', models.TextField(verbose_name='工单内容')),
                ('status', models.IntegerField(choices=[(0, '申请'), (1, '处理中'), (2, '完成'), (3, '拒绝')], default=0, verbose_name='工单状态')),
                ('result_desc', models.TextField(blank=True, null=True, verbose_name='处理结果')),
                ('apply_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('complete_time', models.DateTimeField(auto_now=True, verbose_name='处理完成时间')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_order_applicant', to=settings.AUTH_USER_MODEL, verbose_name='申请人')),
                ('assign_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='指派给')),
                ('final_processor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='final_processor', to=settings.AUTH_USER_MODEL, verbose_name='最终处理人')),
            ],
            options={
                'verbose_name': '工单',
                'verbose_name_plural': '工单',
                'ordering': ['-complete_time'],
            },
        ),
    ]
