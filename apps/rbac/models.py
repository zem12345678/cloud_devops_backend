# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from utils.basemodels import Basemodel

class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    path = models.CharField(max_length=158, null=True, blank=True, verbose_name="链接地址")
    is_frame = models.BooleanField(default=False, verbose_name="外部菜单")
    is_show = models.BooleanField(default=True, verbose_name="显示标记")
    sort = models.IntegerField(null=True, blank=True, verbose_name="排序标记")
    component = models.CharField(max_length=200, null=True, blank=True, verbose_name="组件")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['id']

    # def get_view_permissions(self):
    #     if self.is_superuser:
    #         return Menu.objects.all()
    #     return Menu.objects.filter(groups__in=self.groups.all())

class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="权限名")
    method = models.CharField(max_length=50, null=True, blank=True, verbose_name="方法")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父权限")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']

class Role(models.Model):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField("Permission", blank=True, verbose_name="权限")
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")

class Organization(models.Model):
    """
    组织架构
    """
    organization_type_choices = (
        ("company", "公司"),
        ("department", "部门")
    )
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=organization_type_choices, default="company", verbose_name="类型")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父类组织")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class UserProfile(AbstractUser):
    '''
    用户
    '''
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    image = models.ImageField(upload_to="static/%Y/%m", default="image/vue.gif",
                              max_length=100, null=True, blank=True)
    department = models.ForeignKey("Organization", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门")
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    roles = models.ManyToManyField("Role", verbose_name="角色", blank=True)
    id_rsa_key = models.TextField(null=True)
    id_rsa_pub = models.TextField(null=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

class PerAppName(models.Model):
    app_key = models.CharField("APPkey", max_length=64, null=False, unique=True, help_text="APPkey")
    app_name = models.CharField("APP名称", max_length=32, null=False, blank=False, help_text="APP名称")
    app_desc = models.CharField("APP应用描述", max_length=32, blank=False, help_text="APP应用描述")

    def __str__(self):
        return self.app_name

    class Meta:
        db_table = "pms_app"

class NodeInfo(models.Model):
    node_name = models.CharField("节点名称", max_length=32, db_index=True, help_text="service名称")
    pid = models.IntegerField("节点pid", db_index=True, help_text="pid")
    path_node = models.CharField("节点中文path", max_length=32, db_index=True, help_text="node中文path")
    groups = models.ManyToManyField(Group, verbose_name="用户组关联节点", related_name="node_group", help_text="用户组关联节点")

    def __str__(self):
        return self.node_name

    class Meta:
        db_table = "pms_node"
        ordering = ["id"]

class PmsPermission(models.Model):
    codename = models.CharField("权限简称", max_length=32, help_text="权限简称")
    desc = models.CharField("权限描述信息", max_length=32, help_text="权限描述信息")
    app = models.CharField("APP名称", max_length=32, help_text="APP名称")
    groups = models.ManyToManyField(Group, verbose_name="用户组关联权限", related_name="pms_group", help_text="用户组关联权限")

    def __str__(self):
        return self.codename

    class Meta:
        db_table = 'pms_permission'
        ordering = ['id']

class ApiHttpMethod(Basemodel):

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
class ApiPermission(Basemodel):

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
class ApiPermissionGroup(Basemodel):

    name = models.CharField(max_length=32,
                            unique=True,
                            verbose_name='组名')

    api_permissions    = models.ManyToManyField('ApiPermission',
                                             blank=True,
                                             related_name='api_permissions',
                                             verbose_name=u'API权限')
    users = models.ManyToManyField(UserProfile,
                                  blank=True,
                                  related_name='users',
                                  verbose_name=u'用户')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "api_permission_group"
        verbose_name = "API权限组"
        verbose_name_plural = verbose_name