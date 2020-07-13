
from django.db import models
from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User

from apps.base.models import BaseModel
from apps.user.models import UserProfile

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')



# HTTP请求方式
class ApiHttpMethod(BaseModel):

    method = models.CharField(max_length=32,
                                unique=True,
                                verbose_name='HTTP Method')

    def __str__(self):
        return self.method

    class Meta:
        db_table = "api_http_method"
        verbose_name = "API Method"
        verbose_name_plural = verbose_name



# API权限
class ApiPermission(BaseModel):

    name = models.CharField(max_length=32,
                            unique=True,
                            verbose_name='API名称')

    uri = models.CharField(max_length=100,
                           verbose_name="HTTP URI")

    api_http_methods    = models.ManyToManyField('ApiHttpMethod',
                                             blank=True,
                                             related_name='api_http_methods',
                                             verbose_name=u'API权限')


    def __str__(self):
        return 'Name: {}, Uri: {}'.format(self.name, self.uri)

    class Meta:
        db_table = "api_permission"
        verbose_name = "API权限"
        verbose_name_plural = verbose_name



# API权限组
class ApiPermissionGroup(BaseModel):

    name = models.CharField(max_length=32,
                            unique=True,
                            verbose_name='组名')

    api_permissions    = models.ManyToManyField('ApiPermission',
                                             blank=True,
                                             related_name='api_permissions',
                                             verbose_name=u'API权限')
    users = models.ManyToManyField(AUTH_USER_MODEL,
                                  blank=True,
                                  related_name='users',
                                  verbose_name=u'用户')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "api_permission_group"
        verbose_name = "API权限组"
        verbose_name_plural = verbose_name
