#!/usr/bin/env python
# coding=utf-8
import json
import re
import base64
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore import client
from cloud_devops_backend.settings import ACCCESSKEYID, ACCESSSECRET
from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
from aliyunsdkslb.request.v20140515.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeAvailableResourceRequest import DescribeAvailableResourceRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceTypesRequest import DescribeInstanceTypesRequest
from aliyunsdkecs.request.v20140526.StopInstanceRequest import StopInstanceRequest
from aliyunsdkecs.request.v20140526.StartInstanceRequest import StartInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeDisksRequest import DescribeDisksRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupsRequest import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526.DescribeVpcsRequest import DescribeVpcsRequest
from aliyunsdkecs.request.v20140526.DescribeVSwitchesRequest import DescribeVSwitchesRequest
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest
from aliyunsdkecs.request.v20140526.AllocatePublicIpAddressRequest import AllocatePublicIpAddressRequest
from aliyunsdkecs.request.v20140526 import DescribeImagesRequest, DescribeSecurityGroupsRequest, DescribeVpcsRequest
from aliyunsdkslb.request.v20140515.DescribeVServerGroupsRequest import DescribeVServerGroupsRequest


class ALiYun(object):
    def __init__(self):
        self.AccessKeyId = ACCCESSKEYID
        self.AccessKeySecret = ACCESSSECRET

    def DescribeRegions(self):
        """
        获取所有地域regionId
        :return: {'cn-qingdao': '华北 1'}
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret)
        request = DescribeRegionsRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        res = json.loads(str(response, encoding='utf-8'))
        regions = {}
        for region in res['Regions']['Region']:
            regions[region['RegionId']] = region['LocalName']
        return regions

    def AvailableZones(self, region_id):
        """
        可用区
        :param region_id:  计费方式  地域
        :return:  ['cn-huhehaote-a', 'cn-huhehaote-b']
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        request = DescribeZonesRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        # print(str(response, encoding='utf-8'))
        res = json.loads(str(response, encoding='utf-8'))
        zones = {}
        for zone in res['Zones']['Zone']:
            zones[zone['ZoneId']] = zone['LocalName']
        return zones

    def DescribeAvailableResource(self, InstanceChargeType, region_id, DestinationResource, ZoneId=None):
        """
        可用资源查询接口
        :param region_id:  地域
        :param DestinationResource: 查询的资源类型
        :return:
        """
        resourceclt = client.AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        resourcereq = DescribeAvailableResourceRequest()
        if DestinationResource == 'InstanceType':
            resourcereq.set_ZoneId(ZoneId)
            resourcereq.set_IoOptimized('optimized')
        resourcereq.set_InstanceChargeType(InstanceChargeType)
        resourcereq.set_DestinationResource(DestinationResource)
        resourcereq.set_accept_format('json')
        resourcere = json.loads(resourceclt.do_action_with_exception(resourcereq), encoding='utf-8')
        print(resourcere)
        return resourcere

    def AvailableInstanceType(self, InstanceChargeType, region_id, ZoneId):
        """
        可用实例规格
        :param region_id: 计费方式 地域 可用区
        :return:  计算型:ecs.c5  商用       入门级:ecs.t5
        """
        instanceres = self.DescribeAvailableResource(InstanceChargeType, region_id, 'InstanceType', ZoneId)
        instance = []
        for i in instanceres['AvailableZones']['AvailableZone'][0]['AvailableResources']['AvailableResource'][0][
            'SupportedResources']['SupportedResource']:
            print(i)
            if re.match('ecs.t5', i['Value']) or re.search('ecs.c5', i['Value']) or re.search('ecs.g5', i['Value']):
                instance.append(i['Value'])
        c5 = {
            'ecs.c5.large': '2*4',
            'ecs.c5.xlarge': '4*8',
            'ecs.c5.2xlarge': '8*16',
            'ecs.c5.3xlarge': '12*24',
            'ecs.c5.4xlarge': '16*32',
            'ecs.c5.6xlarge': '24*48',
            'ecs.c5.8xlarge': '32*64',
            'ecs.g5.2xlarge': '8*32'
        }
        t5 = {
            'ecs.t5-lc2m1.nano': '1*0.5',
            'ecs.t5-lc1m2.small': '1*2',
            'ecs.t5-c1m2.large': '2*4',
            'ecs.t5-lc1m4.large': '2*8'
        }
        print(instance)
        for k in list(c5.keys()):
            if k not in instance:
                del c5[k]

        for k in list(t5.keys()):
            if k not in instance:
                del t5[k]
        return c5, t5

    def DescribeImages(self, region_id):
        """
        :param region_id:  地域
        :return:  镜像列表 {'centos_6_09_64_20G_alibase_20180326.vhd': 'CentOS  6.9 64位',}
        """
        imagesclt = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        imagesreq = DescribeImagesRequest.DescribeImagesRequest()
        imagesreq.set_ActionType('DescribeImages')
        imagesreq.set_accept_format('json')
        imagesreq.set_PageSize(100)
        imagesre = json.loads(imagesclt.do_action_with_exception(imagesreq), encoding='utf-8')
        images = {}
        for i in imagesre['Images']['Image']:
            if i['Platform'] == 'CentOS':
                images[i['ImageId']] = i['OSName']
            if i['Platform'] == 'Ubuntu':
                images[i['ImageId']] = i['OSName']
            if i['Platform'] == 'Windows Server 2008':
                images[i['ImageId']] = i['OSName']
            if i['Platform'] == 'Debian':
                images[i['ImageId']] = i['OSName']
        return images

    def DescribeVpcs(self, region_id):
        """
        VPC
        :param region_id:  地域
        :return: {'vpc-hp33ep5m55q5vdebkjpxk': '华北5预发布VPC', 'vpc-hp3xfrxc78pgc0rianhge': '华北5测试'}
        """
        vpcsclt = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        vpcsreq = DescribeVpcsRequest.DescribeVpcsRequest()
        vpcsreq.set_action_name('DescribeVpcs')
        vpcsreq.set_accept_format('json')
        vpcsreq.set_PageSize(50)
        vpcsre = json.loads(vpcsclt.do_action_with_exception(vpcsreq), encoding='utf-8')
        vpcs = {}
        for i in vpcsre['Vpcs']['Vpc']:
            vpcs[i['VpcId']] = i['VpcName']
        return vpcs

    def DescribeVSwitches(self, region_id, zone_id, vpc_id):
        """
        :param region_id:  地域
        :param zone_id:   可用区
        :param vpc_id:  vpc
        :return: {'vsw-hp3ffb8524tt1gqp22utj': '华北5测试B交换机'}
        """
        vswitchesclt = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        vswitchesreq = DescribeVSwitchesRequest()
        vswitchesreq.set_action_name('DescribeVSwitches')
        vswitchesreq.set_VpcId(vpc_id)
        vswitchesreq.set_accept_format('json')
        vswitchesreq.set_PageSize(50)
        vswitchesreq.set_ZoneId(zone_id)
        vswitchesre = json.loads(vswitchesclt.do_action_with_exception(vswitchesreq), encoding='utf-8')
        vswitches = {}
        for i in vswitchesre['VSwitches']['VSwitch']:
            vswitches[i['VSwitchId']] = i['VSwitchName']
        return vswitches

    def DescribeSecurityGroups(self, region_id, vpc_id):
        """
        安全组
        :param region_id:  地域
        :param vpc_id:  vpc
        :return: {'sg-hp3738k45fqqbfja11fl': '华北5测试2', 'sg-hp3hzvhrr2gk8skyo3ul': '华北5测试1'}
        """
        groupsclt = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        groupsreq = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
        groupsreq.set_action_name('DescribeSecurityGroups')
        groupsreq.set_VpcId(vpc_id)
        groupsreq.set_accept_format('json')
        groupsreq.set_PageSize(50)
        groupsre = json.loads(groupsclt.do_action_with_exception(groupsreq), encoding='utf-8')
        groups = {}
        for i in groupsre['SecurityGroups']['SecurityGroup']:
            groups[i['SecurityGroupId']] = i['SecurityGroupName']
        return groups

    def CreateInstance(self, region_id, ZoneId, ImageId, InstanceType, InstanceName, InstanceChargeType,
                       InternetChargeType,
                       InternetMaxBandwidthOut, HostName, DataDisk, Password, VSwitchId, SecurityGroupId,
                       UserData):
        """
        创建 实例
        :param region_id:   地域
        :param ZoneId:  可用区
        :param ImageId: 镜像
        :param InstanceType:  实例模板
        :param InstanceName:  实例名字
        :param InstanceChargeType:  计费方式
        :param InternetChargeType:  网络计费方式
        :param InternetMaxBandwidthOut:  出网带宽
        :param HostName:  主机名字
        :param DataDisk:  数据盘
        :param Password:  密码
        :param VSwitchId: 交换机
        :param SecurityGroupId:  安全组
        :param UserData: 机器初始化cloud_init加载脚本
        :return: {'InstanceId': 'i-2ze210z0uiwyadm1m7x6'}
        """
        createclt = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        createreq = CreateInstanceRequest()
        createreq.set_action_name('CreateInstance')
        createreq.set_accept_format('json')
        createreq.set_ZoneId(ZoneId)
        createreq.set_ImageId(ImageId)
        createreq.set_InstanceType(InstanceType)
        createreq.set_InstanceName(InstanceName)
        createreq.set_InstanceChargeType(InstanceChargeType)
        if InstanceChargeType == 'PrePaid':
            createreq.set_Period('1')
        if InternetChargeType:
            createreq.set_InternetChargeType(InternetChargeType)
            createreq.set_InternetMaxBandwidthOut(InternetMaxBandwidthOut)
        createreq.set_HostName(HostName)
        createreq.set_Password(Password)
        createreq.set_VSwitchId(VSwitchId)
        createreq.set_SecurityGroupId(SecurityGroupId)

        '''通用配置 以下配固定不变配置'''
        createreq.set_KeyPairName('twl-vpc-ecs-key')  # 初始化key
        createreq.set_SecurityEnhancementStrategy('Active')  # 安全加固
        createreq.set_IoOptimized('optimized')  # IO优化

        createreq.set_DataDisks(DataDisk)  # 数据盘

        ''' 通用配置  系统盘 '''
        createreq.set_SystemDiskCategory('cloud_efficiency')  # 高效云盘
        createreq.set_SystemDiskSize(40)  # 系统盘大小40G
        createreq.set_SystemDiskDiskName(HostName + "-sysdisk")  # 系统盘命名

        ''' 初始化要执行的脚本'''
        createreq.set_UserData(UserData)  # 传入UserData数据,进行开机初始化
        createre = json.loads(createclt.do_action_with_exception(createreq), encoding='utf-8')
        return createre

    def stop_instance(self, instanceid):
        """
        停止实例
        :param instanceid:
        :return:
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, instanceid)
        request = StopInstanceRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        res = json.loads(str(response, encoding='utf-8'))
        return res

    def start_instance(self, instanceid):
        """
        启动实例
        :param instanceid:
        :return:
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, instanceid)
        request = StartInstanceRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        res = json.loads(str(response, encoding='utf-8'))
        return res

    def AllocatePublicIpAddress(self, region_id, InstanceId):
        """
        绑定外网IP
        :param region_id:  地域
        :param InstanceId: 实例ID
        :return: {'IpAddress': '39.106.176.130'}
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        request = AllocatePublicIpAddressRequest()
        request.set_accept_format('json')
        request.set_InstanceId(InstanceId)
        response = client.do_action_with_exception(request)
        res = json.loads(response, encoding='utf-8')
        return res

    def get_ecs(self):
        """
        获取所有区域ECS信息
        :return:
        """
        instances = []
        region_ids = self.DescribeRegions()
        for region_id in region_ids.keys():
            client = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id, connect_timeout=30)
            request = DescribeInstancesRequest()
            request.set_accept_format('json')
            response = client.do_action_with_exception(request)
            res = json.loads(str(response, encoding='utf-8'))
            instances += res['Instances']['Instance']
        return instances


    def get_instancetype(self, region_id):
        """
        查看ECS实例规格信息
        :param RegionId:
        :return:
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        request = DescribeInstanceTypesRequest()
        request.set_accept_format('json')
        request.set_InstanceTypeFamily("ecs.t5")
        response = client.do_action_with_exception(request)
        res = str(response, encoding='utf-8')
        return json.loads(res).get("InstanceTypes").get("InstanceType")

    def get_instance_disk_info(self, region_id, zone_id, instance_id):
        """
        获取实例下磁盘信息
        :param regionid: cn-beijing
        :param zoneid: cn-beijing-g
        :param instanceid: i-2ze4wxcyl324952q8m7b
        :return:
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        request = DescribeDisksRequest()
        request.set_accept_format('json')
        request.set_ZoneId(zone_id)
        request.set_InstanceId(instance_id)
        response = client.do_action_with_exception(request)
        # print((str(response, encoding='utf-8')))
        res = json.loads((str(response, encoding='utf-8')))
        return res['Disks']['Disk']

    def get_slb(self):
        """
        获取所有地域下slb负载均衡实例
        :return:
        """
        balancers = []
        regionids = self.DescribeRegions()
        try:
            for rid in regionids:
                client = AcsClient(self.AccessKeyId, self.AccessKeySecret, rid, connect_timeout=30)
                request = DescribeLoadBalancersRequest()
                request.set_accept_format('json')
                response = client.do_action_with_exception(request)
                # print(response)
                res = json.loads(str(response, encoding='utf-8'))
                balancers += res.get("LoadBalancers").get("LoadBalancer")
            return balancers
        except Exception as ex:
            print(ex)

    def get_slb_detail(self, loadbalancer_id, region_id):
        """
        返回lb详细信息
        :param loadbalancerid: lb-2zeqx4f9qglel963dmdzv
        :param regionid: cn-beijing
        :return:
        """
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, region_id)
        request = DescribeLoadBalancerAttributeRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(loadbalancer_id)
        response = client.do_action_with_exception(request)
        return eval(str(response, encoding='utf-8'))

    def DescribeVServerGroups(self):
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, 'cn-beijing')
        request = DescribeVServerGroupsRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId("lb-2zeqx4f9qglel963dmdzv")
        response = client.do_action_with_exception(request)
        # python2:  print(response)
        print(str(response, encoding='utf-8'))

if __name__ == '__main__':
    ali = ALiYun()
    # print(ali.DescribeRegions())
    # print(ali.AvailableZones('cn-beijing'))
    # print(ali.AvailableInstanceType('PostPaid', 'cn-beijing', 'cn-beijing-g'))
    # print(ali.DescribeImages("cn-beijing"))
    # print(ali.DescribeVpcs('cn-beijing'))
    print(ali.DescribeVSwitches('cn-beijing', 'cn-beijing-h', 'vpc-2ze28051lkxec9opj6smj'))
    # print(ali.DescribeSecurityGroups('cn-beijing', 'vpc-2ze28051lkxec9opj6smj'))
    # hostname = "test-01"
    # datadisk = [{"Size": 40, "Category": "cloud_ssd", "DiskName": "ssd-test"},
    #             {"Size": 40, "Category": "cloud_ssd", "DiskName": "ssd-test1"}]
    # cmd = '''#!/bin/sh\n cd  /root;wget http://software.autoadmin.com/init/init.sh  && sh init_vpc.sh > init.log 2>&1'''
    # userdata = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
    # print(userdata)
    # createecs = ali.CreateInstance(region_id='cn-beijing',
    #                                ZoneId='cn-beijing-h',
    #                                ImageId='centos_7_04_64_20G_alibase_201701015.vhd',
    #                                InstanceType='ecs.t5-lc2m1.nano',
    #                                InstanceName=hostname,
    #                                InstanceChargeType='PostPaid',
    #                                InternetChargeType='PayByBandwidth',
    #                                InternetMaxBandwidthOut='1',
    #                                HostName=hostname,
    #                                DataDisk=datadisk,
    #                                Password='1qaz.2wsx',
    #                                VSwitchId='vsw-2ze1c3ty3fj74rr16n1c4',
    #                                SecurityGroupId='sg-2zeg2nvydu16ikvppjm7',
    #                                UserData=userdata)

    # print(ali.get_ecs())
    # print(ali.get_slb())
    # print(ali.get_slb_detail("lb-2zeqx4f9qglel963dmdzv", "cn-beijing"))
    # ali.DescribeVServerGroups()
    # res = ali.get_instancetype("cn-beijing")
    # for i in res:
    #     print(i["CpuCoreCount"],i["MemorySize"])
    # print(ali.get_instance_disk_info("cn-beijing", "cn-beijing-g", "i-2ze4wxcyl324952q8m7b"))
