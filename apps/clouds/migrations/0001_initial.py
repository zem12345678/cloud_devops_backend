# Generated by Django 2.2.3 on 2020-06-06 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackendServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vsgroupname', models.CharField(help_text='虚拟服务器组名称', max_length=100, verbose_name='虚拟服务器组名称')),
                ('remark', models.TextField(blank=True, max_length=500, null=True, verbose_name='备注信息')),
            ],
            options={
                'db_table': 'clouds_slb_backendserver',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(db_index=True, help_text='厂商名称', max_length=32, verbose_name='厂商名称')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=300, null=True, verbose_name='备注')),
            ],
            options={
                'db_table': 'clouds_manufacturer',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SLB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slb_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='SLB名称')),
                ('slb_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='负载均衡id')),
                ('ext_ip', models.CharField(blank=True, max_length=100, null=True, verbose_name='公网ip')),
                ('network', models.CharField(blank=True, help_text='网络类型', max_length=100, null=True, verbose_name='网络类型')),
                ('inner_ip', models.CharField(blank=True, max_length=100, null=True, verbose_name='内网ip')),
                ('protocol', models.CharField(blank=True, help_text='协议类型', max_length=100, null=True, verbose_name='协议类型')),
                ('f_protocol_port', models.CharField(blank=True, max_length=100, null=True, verbose_name='前端协议端口')),
                ('b_protocol_port', models.CharField(blank=True, max_length=100, null=True, verbose_name='后端协议端口')),
                ('status', models.CharField(help_text='SLB状态', max_length=64, verbose_name='SLB状态')),
                ('is_store', models.SmallIntegerField(choices=[(0, '删除'), (1, '保存')], default=1, verbose_name='存储')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('remark', models.TextField(blank=True, max_length=500, null=True, verbose_name='备注信息')),
                ('backend_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clouds.BackendServer', verbose_name='虚拟主机名称')),
                ('cloud_id', models.ForeignKey(help_text='云厂商', on_delete=django.db.models.deletion.CASCADE, to='clouds.Manufacturer', verbose_name='云厂商')),
            ],
            options={
                'db_table': 'clouds_slb',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Instances',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('resource_id', models.CharField(default=None, help_text='资源id', max_length=255, unique=True, verbose_name='资源id')),
                ('region_id', models.CharField(default=None, help_text='地域名称', max_length=255, verbose_name='地域名称')),
                ('instance_id', models.CharField(default=None, help_text='实例ID', max_length=255, verbose_name='实例ID')),
                ('instance_name', models.CharField(default=None, help_text='实例名称', max_length=255, verbose_name='实例名称')),
                ('os_name', models.CharField(default=None, help_text='操作系统', max_length=64, verbose_name='操作系统')),
                ('zone_id', models.CharField(default=None, help_text='可用区', max_length=255, verbose_name='可用区')),
                ('public_ip', models.CharField(db_index=True, help_text='公网ip', max_length=64, null=True, verbose_name='公网ip')),
                ('private_ip', models.CharField(db_index=True, help_text='私有ip', max_length=64, null=True, verbose_name='私有ip')),
                ('e_ip', models.CharField(help_text='弹性ip', max_length=64, null=True, verbose_name='弹性ip')),
                ('instance_status', models.CharField(db_index=True, help_text='实例状态', max_length=64, null=True, verbose_name='实例状态')),
                ('vpc_id', models.CharField(help_text='专有网络', max_length=64, null=True, verbose_name='专有网络')),
                ('cpu_num', models.CharField(default=1, help_text='CPU数', max_length=64, verbose_name='CPU数')),
                ('memory_size', models.CharField(default=1024, help_text='内存大小', max_length=64, verbose_name='内存大小')),
                ('instance_type', models.CharField(default=None, help_text='实例类型', max_length=64, verbose_name='实例类型')),
                ('band_width_out', models.CharField(blank=True, help_text='网络出口带宽', max_length=64, null=True, verbose_name='网络出口带宽')),
                ('instance_charge_type', models.CharField(default='包年包月', help_text='付费类型', max_length=64, verbose_name='付费类型')),
                ('host_name', models.CharField(default=None, help_text='主机名称', max_length=64, verbose_name='主机名称')),
                ('gpu', models.CharField(default=None, help_text='GPU个数', max_length=64, verbose_name='GPU个数')),
                ('ioOptimized', models.CharField(default=None, help_text='IO优化', max_length=64, verbose_name='IO优化')),
                ('create_time', models.CharField(help_text='创建时间', max_length=64, verbose_name='创建时间')),
                ('expire_time', models.CharField(help_text='过期时间', max_length=64, verbose_name='过期时间')),
                ('is_store', models.IntegerField(choices=[(0, '删除'), (1, '保存')], default=1, verbose_name='状态,1:保存,0:删除')),
                ('cloud_id', models.ForeignKey(help_text='云厂商', on_delete=django.db.models.deletion.CASCADE, to='clouds.Manufacturer', verbose_name='云厂商')),
            ],
            options={
                'db_table': 'clouds_instance',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='backendserver',
            name='instance',
            field=models.ForeignKey(max_length=64, on_delete=django.db.models.deletion.CASCADE, to='clouds.Instances', verbose_name='关联主机'),
        ),
    ]