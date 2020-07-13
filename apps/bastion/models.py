#coding:utf-8

from django.db import models


class Account(models.Model):
    username = models.CharField(verbose_name=u"账户名",max_length=50)
    active = models.IntegerField(verbose_name=u"使能",null=True)
    basegroup = models.CharField(verbose_name=u"用户组",max_length=50)
    uid = models.IntegerField(verbose_name=u"uid")
    prikey = models.CharField(verbose_name=u"私钥",max_length=500)
    pubkey = models.CharField(verbose_name=u"公钥",max_length=500)
    appendgroups = models.CharField(verbose_name=u"加入组",max_length=100)
    fullname = models.CharField(verbose_name=u"名字",max_length=50)
    loginshell = models.CharField(verbose_name=u"shell",max_length=20)


    class Meta:
        db_table = "userdb_users_info"


class Groups(models.Model):
    group = models.CharField(verbose_name=u"用户组",max_length=50)
    gid = models.IntegerField(verbose_name=u"Gid")
    class Meta:
        db_table = "userdb_groups"


class Permisssion(models.Model):
    hostname = models.CharField(max_length=50,verbose_name=u"主机IP")
    username = models.CharField(max_length=50,verbose_name=u"用户名")
    appendgroups = models.CharField(max_length=100,verbose_name=u"用户组")
    active = models.BooleanField(verbose_name=u"使能",default=1)


    class Meta:
        db_table = "userdb_host_account"


class Auditor(models.Model):
    exec_time = models.DateTimeField()
    local_ip = models.CharField(max_length=20)
    from_host = models.CharField(max_length=20)
    exec_user = models.CharField(max_length=20)
    login_user = models.CharField(max_length=20)
    exec_pwd = models.CharField(max_length=100)
    ssh_tty = models.CharField(max_length=20)
    command_num = models.CharField(max_length=50)
    command_info = models.CharField(max_length=200)

    class Meta:
        db_table = "audit_records"



class Daemon_sec_sysfile(models.Model):
    file_name = models.CharField(max_length=100)
    file_data = models.TextField(null=True)
    owner_user = models.CharField(max_length=50)
    owner_group = models.CharField(max_length=50)
    mask = models.CharField(max_length=20)
    active = models.BooleanField()

    class Meta:
        db_table  = "daemon_sec_sysfile"


class Daemon_heartbeat(models.Model):
    hostname = models.CharField(max_length=50)
    version = models.CharField(max_length=20,null=True)
    statuscode = models.IntegerField()
    createtime = models.DateTimeField()
    hbtime = models.DateTimeField()

    class Meta:
        db_table = "daemon_heartbeat"
