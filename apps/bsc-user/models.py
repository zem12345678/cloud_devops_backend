from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    name = models.CharField("中文名", max_length=30)
    phone = models.CharField("手机", max_length=11, null=True, blank=True)

    class Meta:
        db_table = "user_profile"
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
