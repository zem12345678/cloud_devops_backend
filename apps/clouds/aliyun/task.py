#!/usr/bin/env python
# coding=utf-8
import os
import django
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud_devops_backend.settings")
django.setup()

import hashlib
from clouds.aliyun.ecs import ALiYun
from clouds.models import Instances, Manufacturer, SLB


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def sync_instances(manufacturer):
    """
    在同步主机之前还需对比阿里云侧和本地机器,根据返回实例名称来新增或删减，来修改status的状态，用来标记已删除或存在
    :param manufacturer: ALY, TXY, AWS
    :return:
    """
    new_list = []
    old_list = []
    # 获取本地数据库所有resource_id
    queryset = Instances.objects.values("resource_id")
    for ins_obj in list(queryset):
        old_list.append(ins_obj['resource_id'])

    ali = ALiYun()
    instances = ali.get_ecs()
    for instance in instances:
        # 获取阿里云所有resource_id
        new_list.append(md5(instance.get('InstanceId')))

    # 阿里云主机多余本地主机
    add_hosts_list = list(set(new_list).difference(set(old_list)))
    if add_hosts_list:
        for instance in instances:
            for manfu_obj in Manufacturer.objects.all():
                if manfu_obj.vendor_name == manufacturer:
                    try:
                        resource_id = md5(instance.get('InstanceId'))
                        host_obj = Instances.objects.get(resource_id=resource_id)
                        host_obj.resource_id = md5(instance.get('InstanceId'))
                        host_obj.region_id = instance.get('RegionId')
                        host_obj.cloud_id_id = manfu_obj.id
                        host_obj.instance_id = instance.get('InstanceId')
                        host_obj.instance_name = instance.get('InstanceName')
                        host_obj.os_name = instance.get('OSName')
                        host_obj.zone_id = instance.get("ZoneId")
                        host_obj.private_ip = instance.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[
                            0]
                        host_obj.public_ip = instance.get('PublicIpAddress').get('IpAddress')[0]
                        host_obj.e_ip = instance.get("EipAddress", "")
                        host_obj.instance_status = instance.get('Status')
                        host_obj.vpc_id = instance.get('InstanceNetworkType')
                        host_obj.cpu_num = instance.get('Cpu')
                        host_obj.memory_size = instance.get('Memory')
                        host_obj.ioOptimized = instance.get('IoOptimized')
                        host_obj.instance_type = instance.get('InstanceType')
                        host_obj.band_width_out = instance.get('InternetMaxBandwidthOut')
                        host_obj.instance_charge_type = instance.get('InstanceChargeType')
                        host_obj.host_name = instance.get('HostName')
                        host_obj.gpu = instance.get('GPUAmount')
                        host_obj.create_time = instance.get('CreationTime')
                        host_obj.expire_time = instance.get('ExpiredTime')
                        host_obj.save()

                    except Instances.DoesNotExist:
                        Instances.objects.create(resource_id=md5(instance.get('InstanceId')),
                                                 region_id=instance.get('RegionId'),
                                                 cloud_id_id=manfu_obj.id,
                                                 instance_name=instance.get('InstanceName'),
                                                 os_name=instance.get('OSName'),
                                                 zone_id=instance.get("ZoneId"),
                                                 instance_id=instance.get('InstanceId'),
                                                 private_ip=
                                                 instance.get('VpcAttributes').get('PrivateIpAddress').get(
                                                     'IpAddress', "")[0],
                                                 public_ip=instance.get('PublicIpAddress').get('IpAddress')[0],
                                                 e_ip=instance.get("EipAddress", ""),
                                                 instance_status=instance.get('Status'),
                                                 vpc_id=instance.get('InstanceNetworkType'),
                                                 cpu_num=instance.get('Cpu'),
                                                 memory_size=instance.get('Memory'),
                                                 ioOptimized=instance.get('IoOptimized'),
                                                 instance_type=instance.get('InstanceType'),
                                                 band_width_out=instance.get('InternetMaxBandwidthOut'),
                                                 instance_charge_type=instance.get('InstanceChargeType'),
                                                 host_name=instance.get('HostName'),
                                                 gpu=instance.get('GPUAmount'),
                                                 create_time=instance.get('CreationTime'),
                                                 expire_time=instance.get('ExpiredTime')
                                                 )

    # 本地主机多余阿里云主机,将本地主机状态置为2
    delete_host_list = list(set(old_list).difference(set(new_list)))
    if delete_host_list:
        for host_id in delete_host_list:
            ins_obj = Instances.objects.get(resource_id=host_id)
            ins_obj.status = 2
            ins_obj.save()


def sync_slb(manufacturer):
    """
    在同步主机之前还需对比阿里云侧和本地机器,根据返回负载均衡名称来新增或删减，来修改status的状态，用来标记已删除或存在
    :param manufacturer: ALY, TXY, AWS
    :return:
    """
    new_list = []
    old_list = []
    # 获取本地数据库所有slb_id
    queryset = SLB.objects.values("slb_id")
    for slb_obj in list(queryset):
        old_list.append(slb_obj['slb_id'])

    ali = ALiYun()
    loadbalancers = ali.get_slb()
    for lb_obj in loadbalancers:
        # 获取阿里云所有resource_id
        new_list.append(lb_obj.get('LoadBalancerId'))

    # 阿里云主机多余本地主机
    add_hosts_list = list(set(new_list).difference(set(old_list)))

    if add_hosts_list:
        for instance in loadbalancers:
            for manfu_obj in Manufacturer.objects.all():
                if manfu_obj.vendor_name == manufacturer:
                    try:
                        slb_id = instance.get("LoadBalancerId")
                        slb_obj = SLB.objects.get(slb_id=slb_id)
                        slb_obj.slb_id = slb_id
                        slb_obj.slb_name = instance.get('LoadBalancerName')
                        slb_obj.ext_ip = instance.get('Address', "")
                        slb_obj.inner_ip = instance.get('Address', "")
                        slb_obj.network = instance.get('NetworkType')
                        slb_obj.cloud_id_id = manfu_obj.id
                        slb_obj.status = instance.get('LoadBalancerStatus', "")
                        slb_obj.backend_server_id = 1
                        slb_obj.save()
                    except SLB.DoesNotExist:
                        SLB.objects.create(slb_id=instance.get("LoadBalancerId"),
                                           slb_name=instance.get('LoadBalancerName'),
                                           ext_ip=instance.get('Address', ""),
                                           inner_ip=instance.get('Address', ""),
                                           network=instance.get('NetworkType'),
                                           cloud_id_id=manfu_obj.id,
                                           status=instance.get('LoadBalancerStatus', ""),
                                           backend_server_id=1)


if __name__ == '__main__':
    # sync_instances("ALY")
    sync_slb("ALY")
