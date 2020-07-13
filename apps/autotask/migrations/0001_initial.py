# Generated by Django 2.2.3 on 2020-06-06 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='任务名称')),
                ('playbook', models.FileField(upload_to='playbook/%Y/%m', verbose_name='playbook文件')),
                ('detail_result', models.TextField(blank=True, null=True, verbose_name='执行结果详情')),
                ('status', models.CharField(choices=[('Y', '已执行'), ('N', '未执行')], default='N', max_length=1, verbose_name='执行状态')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')),
                ('exec_time', models.DateTimeField(auto_now=True, verbose_name='执行时间')),
            ],
            options={
                'verbose_name': '任务',
                'verbose_name_plural': '任务',
                'ordering': ['-add_time'],
            },
        ),
    ]
