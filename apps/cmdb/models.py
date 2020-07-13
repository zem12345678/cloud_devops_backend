from django.db import models
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
import django.utils.timezone as timezone
from django_mysql.models import JSONField
from datetime import datetime
def JSONFieldDefault():
    return {}

User = get_user_model()

class AbstractMode(models.Model):
    pid = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name='child'
    )

    class Meta:
        abstract = True
        app_label = 'cmdb'

class Dict(AbstractMode):
    key = models.CharField(max_length=80, verbose_name='键')
    value = models.CharField(max_length=80, verbose_name='值')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '字典'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'

class TimeAbstract(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True
        app_label = 'cmdb'

class DeviceAbstract(models.Model):
    status = models.CharField(max_length=10, blank=True, default='', verbose_name='状态')
    sys_hostname = models.CharField(max_length=100, blank=True, default='', verbose_name='主机名')
    mac_address = models.CharField(max_length=150, blank=True, default='', verbose_name='MAC地址')
    sn_number = models.CharField(max_length=150, blank=True, default='', verbose_name='SN号码')
    os_type = models.CharField(max_length=50, blank=True, default='', verbose_name='系统类型')
    os_version = models.CharField(max_length=100, blank=True, default='', verbose_name='系统版本')
    device_type = models.CharField(max_length=50, blank=True, default='', verbose_name='设备类型')
    device_model = models.CharField(max_length=150, blank=True, default='', verbose_name='设备型号')

    class Meta:
        abstract = True
        app_label = 'cmdb'

class ConnectionAbstract(models.Model):
    hostname = models.CharField(max_length=80, verbose_name='IP/域名')
    auth_type = models.CharField(max_length=30, default='',verbose_name='认证类型')
    port = models.IntegerField(blank=True, default=0, verbose_name='端口')
    username = models.CharField(max_length=50, blank=True, default='', verbose_name='用户名/key')
    password = models.CharField(max_length=80, blank=True, default='', verbose_name='密码')


    class Meta:
        abstract = True
        app_label = 'cmdb'

class ConnectionInfo(ConnectionAbstract, TimeAbstract):
    is_public = models.BooleanField(default=False, verbose_name="是否公开")
    desc = models.CharField(max_length=150, blank=True, null=True, verbose_name='备注')
    uid = models.ForeignKey(User, null=True, blank=True, default=1, on_delete=models.SET_NULL, verbose_name='关联用户')

    class Meta:
        verbose_name = '连接信息'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'

class DeviceScanInfo(DeviceAbstract, ConnectionAbstract, TimeAbstract):
    '''
    储存扫描成功后的设备信息临时表
    '''
    error_message = models.TextField(max_length=150, blank=True, default='', verbose_name='错误信息')

    class Meta:
        verbose_name = '扫描信息'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'

class DeviceInfo(AbstractMode, DeviceAbstract, TimeAbstract):
    '''
    资产信息表
    '''
    auth_type = models.CharField(max_length=30, default='', verbose_name='认证类型')
    hostname = models.CharField(max_length=50, verbose_name='IP/域名')
    network_type = models.IntegerField(blank=True, null=True, verbose_name='网络类型')
    leader = models.CharField(max_length=50,blank=True, null=True, verbose_name='责任人')
    buy_date = models.DateField(default=datetime.now, verbose_name="购买日期")
    warranty_date = models.DateField(default=datetime.now, verbose_name="到保日期")
    desc = models.TextField(blank=True, default='', verbose_name='备注信息')
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    businesses = models.ManyToManyField("Business", blank=True, verbose_name="业务")
    groups = models.ManyToManyField("DeviceGroup", blank=True, verbose_name="设备组")
    labels = models.ManyToManyField("Label", blank=True, verbose_name="标签")
    history = HistoricalRecords(excluded_fields=['add_time', 'modify_time', 'pid'])

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

class Business(TimeAbstract):
    name = models.CharField(max_length=50, verbose_name='业务名称')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '业务'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'

class DeviceGroup(TimeAbstract):
    name = models.CharField(max_length=50, verbose_name='组名')
    alias = models.CharField(default='', max_length=100, verbose_name='别名')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '设备组'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'

class Label(TimeAbstract):
    name = models.CharField(max_length=50, verbose_name='标签名')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'


class DeviceFile(TimeAbstract):
    device = models.ForeignKey('DeviceInfo', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='设备')
    file_content = models.FileField(upload_to="conf/asset_file/%Y/%m", null=True, blank=True, verbose_name="资产文件")
    upload_user = models.CharField(max_length=20, verbose_name="上传人")

    class Meta:
        verbose_name = '设备文件'
        verbose_name_plural = verbose_name
        app_label = 'cmdb'



class Classification(models.Model):
    """ 分类表 """

    name = models.CharField(verbose_name="名称", max_length=128, unique=True)
    remarks = models.CharField(verbose_name="备注", max_length=1024)
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "cmdb_classification"
        verbose_name = "分类管理"
        verbose_name_plural = "分类管理"
        app_label = 'cmdb'



class Table(models.Model):
    """ 表管理 """

    name = models.CharField(verbose_name="名称", max_length=128)
    alias = models.CharField(verbose_name="别名", max_length=128)
    classification = models.ForeignKey("Classification", on_delete=models.CASCADE)
    fields = JSONField(default=JSONFieldDefault)
    remarks = models.CharField(verbose_name="备注", max_length=1024)
    self = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return self.alias

    class Meta:
        db_table = "cmdb_table"
        verbose_name = "表管理"
        verbose_name_plural = "表管理"
        app_label = 'cmdb'



class Data(models.Model):
    """ 数据管理 """

    table = models.ForeignKey("Table", on_delete=models.CASCADE)
    value = JSONField(default=JSONFieldDefault)
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return self.table.alias

    class Meta:
        db_table = "cmdb_data"
        verbose_name = "数据管理"
        verbose_name_plural = "数据管理"
        app_label = 'cmdb'

