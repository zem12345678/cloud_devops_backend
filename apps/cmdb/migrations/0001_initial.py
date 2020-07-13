# Generated by Django 2.2.3 on 2020-05-31 10:00

import cmdb.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_mysql.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=50, verbose_name='业务名称')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '业务',
                'verbose_name_plural': '业务',
            },
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='名称')),
                ('remarks', models.CharField(max_length=1024, verbose_name='备注')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '分类管理',
                'verbose_name_plural': '分类管理',
                'db_table': 'cmdb_classification',
            },
        ),
        migrations.CreateModel(
            name='DeviceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=50, verbose_name='组名')),
                ('alias', models.CharField(default='', max_length=100, verbose_name='别名')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '设备组',
                'verbose_name_plural': '设备组',
            },
        ),
        migrations.CreateModel(
            name='DeviceScanInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.CharField(blank=True, default='', max_length=10, verbose_name='状态')),
                ('sys_hostname', models.CharField(blank=True, default='', max_length=100, verbose_name='主机名')),
                ('mac_address', models.CharField(blank=True, default='', max_length=150, verbose_name='MAC地址')),
                ('sn_number', models.CharField(blank=True, default='', max_length=150, verbose_name='SN号码')),
                ('os_type', models.CharField(blank=True, default='', max_length=50, verbose_name='系统类型')),
                ('os_version', models.CharField(blank=True, default='', max_length=100, verbose_name='系统版本')),
                ('device_type', models.CharField(blank=True, default='', max_length=50, verbose_name='设备类型')),
                ('device_model', models.CharField(blank=True, default='', max_length=150, verbose_name='设备型号')),
                ('hostname', models.CharField(max_length=80, verbose_name='IP/域名')),
                ('auth_type', models.CharField(default='', max_length=30, verbose_name='认证类型')),
                ('port', models.IntegerField(blank=True, default=0, verbose_name='端口')),
                ('username', models.CharField(blank=True, default='', max_length=50, verbose_name='用户名/key')),
                ('password', models.CharField(blank=True, default='', max_length=80, verbose_name='密码')),
                ('error_message', models.TextField(blank=True, default='', max_length=150, verbose_name='错误信息')),
            ],
            options={
                'verbose_name': '扫描信息',
                'verbose_name_plural': '扫描信息',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=50, verbose_name='标签名')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('alias', models.CharField(max_length=128, verbose_name='别名')),
                ('fields', django_mysql.models.JSONField(default=cmdb.models.JSONFieldDefault)),
                ('remarks', models.CharField(max_length=1024, verbose_name='备注')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('classification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Classification')),
                ('self', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Table')),
            ],
            options={
                'verbose_name': '表管理',
                'verbose_name_plural': '表管理',
                'db_table': 'cmdb_table',
            },
        ),
        migrations.CreateModel(
            name='HistoricalDeviceInfo',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='', max_length=10, verbose_name='状态')),
                ('sys_hostname', models.CharField(blank=True, default='', max_length=100, verbose_name='主机名')),
                ('mac_address', models.CharField(blank=True, default='', max_length=150, verbose_name='MAC地址')),
                ('sn_number', models.CharField(blank=True, default='', max_length=150, verbose_name='SN号码')),
                ('os_type', models.CharField(blank=True, default='', max_length=50, verbose_name='系统类型')),
                ('os_version', models.CharField(blank=True, default='', max_length=100, verbose_name='系统版本')),
                ('device_type', models.CharField(blank=True, default='', max_length=50, verbose_name='设备类型')),
                ('device_model', models.CharField(blank=True, default='', max_length=150, verbose_name='设备型号')),
                ('auth_type', models.CharField(default='', max_length=30, verbose_name='认证类型')),
                ('hostname', models.CharField(max_length=50, verbose_name='IP/域名')),
                ('network_type', models.IntegerField(blank=True, null=True, verbose_name='网络类型')),
                ('leader', models.CharField(blank=True, max_length=50, null=True, verbose_name='责任人')),
                ('buy_date', models.DateField(default=datetime.datetime.now, verbose_name='购买日期')),
                ('warranty_date', models.DateField(default=datetime.datetime.now, verbose_name='到保日期')),
                ('desc', models.TextField(blank=True, default='', verbose_name='备注信息')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical 设备信息',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Dict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=80, verbose_name='键')),
                ('value', models.CharField(max_length=80, verbose_name='值')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='cmdb.Dict')),
            ],
            options={
                'verbose_name': '字典',
                'verbose_name_plural': '字典',
            },
        ),
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.CharField(blank=True, default='', max_length=10, verbose_name='状态')),
                ('sys_hostname', models.CharField(blank=True, default='', max_length=100, verbose_name='主机名')),
                ('mac_address', models.CharField(blank=True, default='', max_length=150, verbose_name='MAC地址')),
                ('sn_number', models.CharField(blank=True, default='', max_length=150, verbose_name='SN号码')),
                ('os_type', models.CharField(blank=True, default='', max_length=50, verbose_name='系统类型')),
                ('os_version', models.CharField(blank=True, default='', max_length=100, verbose_name='系统版本')),
                ('device_type', models.CharField(blank=True, default='', max_length=50, verbose_name='设备类型')),
                ('device_model', models.CharField(blank=True, default='', max_length=150, verbose_name='设备型号')),
                ('auth_type', models.CharField(default='', max_length=30, verbose_name='认证类型')),
                ('hostname', models.CharField(max_length=50, verbose_name='IP/域名')),
                ('network_type', models.IntegerField(blank=True, null=True, verbose_name='网络类型')),
                ('leader', models.CharField(blank=True, max_length=50, null=True, verbose_name='责任人')),
                ('buy_date', models.DateField(default=datetime.datetime.now, verbose_name='购买日期')),
                ('warranty_date', models.DateField(default=datetime.datetime.now, verbose_name='到保日期')),
                ('desc', models.TextField(blank=True, default='', verbose_name='备注信息')),
                ('businesses', models.ManyToManyField(blank=True, to='cmdb.Business', verbose_name='业务')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, to='cmdb.DeviceGroup', verbose_name='设备组')),
                ('labels', models.ManyToManyField(blank=True, to='cmdb.Label', verbose_name='标签')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='cmdb.DeviceInfo')),
            ],
            options={
                'verbose_name': '设备信息',
                'verbose_name_plural': '设备信息',
            },
        ),
        migrations.CreateModel(
            name='DeviceFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('file_content', models.FileField(blank=True, null=True, upload_to='conf/asset_file/%Y/%m', verbose_name='资产文件')),
                ('upload_user', models.CharField(max_length=20, verbose_name='上传人')),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmdb.DeviceInfo', verbose_name='设备')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', django_mysql.models.JSONField(default=cmdb.models.JSONFieldDefault)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Table')),
            ],
            options={
                'verbose_name': '数据管理',
                'verbose_name_plural': '数据管理',
                'db_table': 'cmdb_data',
            },
        ),
        migrations.CreateModel(
            name='ConnectionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('hostname', models.CharField(max_length=80, verbose_name='IP/域名')),
                ('auth_type', models.CharField(default='', max_length=30, verbose_name='认证类型')),
                ('port', models.IntegerField(blank=True, default=0, verbose_name='端口')),
                ('username', models.CharField(blank=True, default='', max_length=50, verbose_name='用户名/key')),
                ('password', models.CharField(blank=True, default='', max_length=80, verbose_name='密码')),
                ('is_public', models.BooleanField(default=False, verbose_name='是否公开')),
                ('desc', models.CharField(blank=True, max_length=150, null=True, verbose_name='备注')),
                ('uid', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '连接信息',
                'verbose_name_plural': '连接信息',
            },
        ),
    ]
