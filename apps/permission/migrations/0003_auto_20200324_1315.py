# Generated by Django 2.2 on 2020-03-24 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0002_apipermissiongroup_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apihttpmethod',
            options={'verbose_name': 'API Method', 'verbose_name_plural': 'API Method'},
        ),
    ]
