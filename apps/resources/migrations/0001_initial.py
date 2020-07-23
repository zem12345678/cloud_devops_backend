# Generated by Django 2.2.3 on 2020-06-04 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.CharField(help_text='idc字母简称', max_length=10, unique=True, verbose_name='idc字母简称')),
                ('name', models.CharField(help_text='idc名称', max_length=30, verbose_name='idc名称')),
                ('address', models.CharField(blank=True, help_text='idc具体地址', max_length=255, null=True, verbose_name='idc具体地址')),
                ('tel', models.CharField(blank=True, help_text='客服电话', max_length=15, null=True, verbose_name='客服电话')),
                ('mail', models.EmailField(blank=True, help_text='联系人邮箱', max_length=255, null=True, verbose_name='联系人邮箱')),
                ('remark', models.CharField(blank=True, help_text='备注说明', max_length=255, null=True, verbose_name='备注说明')),
            ],
            options={
                'verbose_name': '机房信息',
                'verbose_name_plural': '机房信息',
                'db_table': 'resources_idc',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(db_index=True, help_text='厂商名称', max_length=32, verbose_name='厂商名称')),
                ('tel', models.CharField(help_text='联系电话', max_length=20, null=True, verbose_name='联系电话')),
                ('mail', models.EmailField(blank=True, help_text='联系邮箱', max_length=254, null=True, verbose_name='email')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=300, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '厂商信息',
                'verbose_name_plural': '厂商信息',
                'db_table': 'resources_manufacturer',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(help_text='型号名称', max_length=32, verbose_name='型号名称')),
                ('vendor', models.ForeignKey(help_text='所属制造商', on_delete=django.db.models.deletion.CASCADE, to='resources.Manufacturer', verbose_name='所属制造商')),
            ],
            options={
                'verbose_name': '型号信息',
                'verbose_name_plural': '型号信息',
                'db_table': 'resources_productmodel',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='机柜名称', max_length=50, verbose_name='机柜名称')),
                ('power_supply', models.IntegerField(help_text='电源功率', verbose_name='电源功率')),
                ('idc', models.ForeignKey(help_text='所在机房', on_delete=django.db.models.deletion.CASCADE, to='resources.Idc', verbose_name='所在机房')),
            ],
            options={
                'verbose_name': '机柜信息',
                'verbose_name_plural': '机柜信息',
                'db_table': 'resources_cabinet',
                'ordering': ['id'],
            },
        ),
    ]