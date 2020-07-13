import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Name")
    users = models.ManyToManyField("users.User", related_name='related_user_orgs', blank=True)
    created_by = models.CharField(max_length=32, null=True, blank=True, verbose_name='Created by')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Date created')
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name='Comment')

    class Meta:
        verbose_name = "用户角色管理"

    def __str__(self):
        return self.name
