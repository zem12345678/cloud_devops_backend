# Generated by Django 2.2 on 2020-03-16 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiHttpMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('method', models.CharField(max_length=32, unique=True, verbose_name='HTTP Method')),
            ],
            options={
                'verbose_name': 'API HTTP Method',
                'verbose_name_plural': 'API HTTP Method',
                'db_table': 'api_http_method',
            },
        ),
        migrations.CreateModel(
            name='ApiPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='API名称')),
                ('uri', models.CharField(max_length=100, verbose_name='HTTP URI')),
                ('api_http_methods', models.ManyToManyField(blank=True, related_name='api_http_methods', to='permission.ApiHttpMethod', verbose_name='API权限')),
            ],
            options={
                'verbose_name': 'API权限',
                'verbose_name_plural': 'API权限',
                'db_table': 'api_permission',
            },
        ),
        migrations.CreateModel(
            name='ApiPermissionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='组名')),
                ('api_permissions', models.ManyToManyField(blank=True, related_name='api_permissions', to='permission.ApiPermission', verbose_name='API权限')),
            ],
            options={
                'verbose_name': 'API权限组',
                'verbose_name_plural': 'API权限组',
                'db_table': 'api_permission_group',
            },
        ),
    ]
