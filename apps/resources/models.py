from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Manufacturer(models.Model):
    vendor_name     = models.CharField("厂商名称", max_length=32, db_index=True, help_text="厂商名称")
    tel             = models.CharField("联系电话", null=True, max_length=20, help_text="联系电话")
    mail            = models.EmailField("email", null=True, blank=True, help_text="联系邮箱")
    remark          = models.CharField("备注", max_length=300, null=True, blank=True, help_text="备注")

    def __str__(self):
        return self.vendor_name

    class Meta:
        db_table = 'resources_manufacturer'
        # permissions = (
        #     ("view_manufacturer", "cat view manufacturer"),
        # )
        verbose_name = '厂商信息'
        verbose_name_plural = verbose_name
        ordering = ["id"]
        app_label = 'resources'

class ProductModel(models.Model):
    model_name      = models.CharField("型号名称", max_length=32, help_text="型号名称")
    vendor          = models.ForeignKey(Manufacturer, verbose_name="所属制造商", help_text="所属制造商",on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name

    class Meta:
        db_table = 'resources_productmodel'
        # permissions = (
        #     ("view_productmodel", "cat view productmodel"),
        # )
        verbose_name = '型号信息'
        verbose_name_plural = verbose_name
        ordering = ["id"]
        app_label = 'resources'

class Idc(models.Model):
    letter          = models.CharField("idc字母简称", max_length=10, unique=True, help_text="idc字母简称")
    name            = models.CharField("idc名称", max_length=30, help_text="idc名称")
    address         = models.CharField("idc具体地址", max_length=255, null=True, blank=True, help_text="idc具体地址")
    tel             = models.CharField("客服电话", max_length=15, null=True, blank=True, help_text="客服电话")
    mail            = models.EmailField("联系人邮箱", max_length=255, null=True, blank=True, help_text="联系人邮箱")
    remark          = models.CharField("备注说明", max_length=255, null=True, blank=True, help_text="备注说明")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resources_idc'
        # permissions = (
        #     ("view_idc", "cat view idc"),
        # )
        verbose_name = '机房信息'
        verbose_name_plural = verbose_name
        ordering = ["id"]
        app_label = 'resources'

class Cabinet(models.Model):
    name            = models.CharField("机柜名称", max_length=50, help_text="机柜名称")
    power_supply    = models.IntegerField("电源功率", help_text="电源功率")
    idc             = models.ForeignKey(Idc, verbose_name="所在机房", help_text="所在机房",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resources_cabinet'
        verbose_name = '机柜信息'
        verbose_name_plural = verbose_name
        # permissions = (
        #     ("view_cabinet", "cat view cabinet"),
        # )
        ordering = ["id"]
        app_label = 'resources'

class Product(models.Model):
    service_name    = models.CharField("业务线名称", max_length=32, help_text="业务线名称")
    pid             = models.IntegerField("上级业务线id", db_index=True, help_text="上级业务线id")
    module_letter   = models.CharField("业务线字母简称", max_length=32, help_text="业务线字母简称")
    dev_interface   = models.ManyToManyField(User, verbose_name="开发接口人", related_name="dev_interface", help_text="开发接口人")
    op_interface    = models.ManyToManyField(User, verbose_name="运维接口人", related_name="op_interface", help_text="运维接口人")

    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'resources_product'
        # permissions = (
        #     ("view_product", "can view products"),
        # )
        verbose_name = '业务线'
        verbose_name_plural = verbose_name
        ordering = ["id"]
        app_label = 'resources'

class Server(models.Model):
    manufacturer    = models.ForeignKey(Manufacturer, verbose_name="制造商", null=True, help_text="制造商",on_delete=models.CASCADE)
    manufacture_data= models.DateField("制造日期", null=True, help_text="制造日期")
    model_name      = models.ForeignKey(ProductModel, verbose_name="服务器型号", default=None, help_text="服务器型号",on_delete=models.CASCADE)
    idc             = models.ForeignKey(Idc, verbose_name="所在机房", null=True, help_text="所在机房",on_delete=models.CASCADE)
    cabinet         = models.ForeignKey(Cabinet, verbose_name="所在机柜", null=True, help_text="所在机柜",on_delete=models.CASCADE)
    cabinet_position= models.CharField("机柜内位置", max_length=32, null=True, help_text="机柜内位置")
    warranty_time   = models.DateField("保修时间", null=True, help_text="保修时间")
    purchasing_time = models.DateField("采购时间", null=True, help_text="采购时间")
    power_supply    = models.IntegerField("电源功率", null=True, help_text="电源功率")
    os              = models.CharField("操作系统", max_length=100, default=None, help_text="操作系统")
    hostname        = models.CharField("主机名", max_length=50, default=None, db_index=True, help_text="主机名")
    manage_ip       = models.CharField("管理IP", max_length=32, default=None, db_index=True, help_text="管理IP")
    server_cpu      = models.CharField("CPU信息", max_length=250, default=None, help_text="CPU信息")
    disk            = models.CharField("硬盘信息", max_length=300, null=True, help_text="硬盘信息")
    server_mem      = models.CharField("内存信息", max_length=100, default=None, help_text="内存信息")
    status          = models.CharField("服务器状态", max_length=32, null=True, db_index=True, help_text="服务器状态")
    remark          = models.TextField("备注", null=True, help_text="备注")
    service         = models.ForeignKey(Product, null=True, verbose_name="一级业务线", related_name="service", help_text="一级业务线",on_delete=models.CASCADE)
    server_purpose  = models.ForeignKey(Product, null=True, verbose_name="二级产品线", related_name="server_purpose", help_text="二级产品线",on_delete=models.CASCADE)
    last_check      = models.DateTimeField("上次检测时间", auto_now=True, help_text="上次检测时间")
    uuid            = models.CharField("UUID", max_length=100, db_index=True,null=True, unique=True, help_text="UUID")
    sn              = models.CharField("SN", max_length=40,db_index=True,null=True, help_text="SN")
    rmt_card_ip     = models.CharField("远程管理卡IP", max_length=15, null=True, help_text="远程管理卡IP")
    server_type     = models.IntegerField("机器类型", db_index=True, default=0, help_text="机器类型")
    """
        机器类型，0：vm, 1:物理机, 2:宿主机
    """

    def __str__(self):
        return "{}[{}]".format(self.hostname, self.manage_ip)

    class Meta:
        db_table = 'resources_server'
        # permissions=(
        #     ("view_server", "cat view server"),
        # )
        verbose_name = '机器信息'
        verbose_name_plural = verbose_name
        app_label = 'resources'

class NetworkDevice(models.Model):
    """
    网卡模型
    """
    name        = models.CharField("网卡设备名", max_length=32)
    mac         = models.CharField("网卡mac地址", max_length=32)
    host        = models.ForeignKey(Server, verbose_name="所在服务器",on_delete=models.CASCADE)
    remark      = models.CharField("备注", max_length=300, null=True)

    def __str__(self):
        return "{}[{}]".format(self.name, self.host)
    class Meta:
        db_table = 'resources_networkdevice'
        # permissions=(
        #     ("view_networkdevice", "cat view networkdevice"),
        # )
        verbose_name = '网卡信息'
        verbose_name_plural = verbose_name
        app_label = 'resources'

class IP(models.Model):
    ip_addr     = models.CharField("ip地址", max_length=20, db_index=True)
    netmask     = models.CharField("子网掩码", max_length=20)
    device      = models.ForeignKey(NetworkDevice, verbose_name="网卡",on_delete=models.CASCADE)

    def __str__(self):
        return self.ip_addr

    class Meta:
        db_table = 'resources_ip'
        # permissions=(
        #     ("view_ip", "cat view ip"),
        # )
        verbose_name = 'IP'
        verbose_name_plural = verbose_name
        app_label = 'resources'

