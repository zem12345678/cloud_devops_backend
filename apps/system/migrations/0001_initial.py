# Generated by Django 2.2.14 on 2020-09-19 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgentApprovalList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_id', models.CharField(max_length=128, verbose_name='AGENT ID')),
                ('ipaddress', models.CharField(blank=True, max_length=256, null=True, verbose_name='IP地址')),
                ('hostname', models.CharField(blank=True, max_length=128, null=True, verbose_name='主机名称')),
                ('apply_time', models.DateTimeField(blank=True, null=True, verbose_name='agent申请时间')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'Agent注册审批',
                'verbose_name_plural': 'Agent注册审批',
                'db_table': 'system_agent_approval',
            },
        ),
        migrations.CreateModel(
            name='AgentList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_id', models.CharField(max_length=128, verbose_name='AGENT ID')),
                ('ipaddress', models.CharField(blank=True, max_length=256, null=True, verbose_name='IP地址')),
                ('hostname', models.CharField(blank=True, max_length=128, null=True, verbose_name='主机名称')),
                ('apply_time', models.DateTimeField(blank=True, null=True, verbose_name='agent申请时间')),
                ('last_heartbeat', models.DateTimeField(blank=True, null=True, verbose_name='最后一次心跳时间')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'Agent列表',
                'verbose_name_plural': 'Agent列表',
                'db_table': 'system_agent_list',
            },
        ),
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_id', models.CharField(max_length=128, verbose_name='AGENT ID')),
                ('ipaddress', models.CharField(blank=True, max_length=256, null=True, verbose_name='IP地址')),
                ('hostname', models.CharField(blank=True, max_length=128, null=True, verbose_name='主机名称')),
                ('apply_time', models.DateTimeField(blank=True, null=True, verbose_name='agent申请时间')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'Agent黑名单',
                'verbose_name_plural': 'Agent黑名单',
                'db_table': 'system_blacklist',
            },
        ),
    ]
