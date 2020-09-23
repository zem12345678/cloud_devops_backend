# @Time    : 2020/9/19 19:52
# @Author  : ZhangEnmin
# @FileName: group_serializer.py
# @Software: PyCharm
from django.contrib.auth.models import Group
from ..models import PmsPermission,UserProfile
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    """
    用户组序列化类
    """

    def get_node(self, node_queryset):
        ret = []
        for node in node_queryset:
            ret.append(node.node_name)
        return ret

    def get_permissions(self, permission_queryset):
        ret = []
        for per in permission_queryset:
            ret.append(per.codename)
        return ret

    def get_users(self, users_queryset):
        ret = []
        for u in users_queryset:
            ret.append(u.username)
        return ret

    def to_representation(self, instance):
        nodes = self.get_node(instance.node_group.all())
        permissions = self.get_permissions(instance.pms_group.all())
        member = self.get_users(instance.user_set.all())
        ret = super(GroupSerializer, self).to_representation(instance)
        # ret["nodes"] = nodes
        ret["permissions"] = permissions
        ret["member"] = member
        return ret

    class Meta:
        model = Group
        fields = ("id", "name")

class GroupMembersSerizlizer(serializers.Serializer):
    uids = serializers.ListField(required=True)

    def validate_uids(self, uids):
        userIds = []
        objs = UserProfile.objects.filter(pk__in=uids)
        for obj in objs:
            userIds.append(str(obj.id))
        if userIds != uids:
            raise serializers.ValidationError("uid 错误")
        return objs

class GroupPermissionSerizlizer(serializers.Serializer):
    pids = serializers.ListField(required=True)

    def validate_uids(self, pids):
        perIds = []
        objs = PmsPermission.objects.filter(pk__in=pids)
        for obj in objs:
            perIds.append(str(obj.id))
        if perIds != pids:
            raise serializers.ValidationError("pid 错误")
        return objs

class UserGroupsSerializer(serializers.ModelSerializer):
    """
    用户的角色 序列化类
    """
    groups = GroupSerializer(many=True)

    def to_representation(self, instance):
        name = instance.name
        ret = super(UserGroupsSerializer, self).to_representation(instance)
        ret["name"] = name
        return ret

    class Meta:
        model = UserProfile
        fields = ("id", "username", "groups")


# class Groupserializer(serializers.ModelSerializer):
#     """
#     group序列化类
#     """
#     def to_representation(self, instance):
#         member = instance.user_set.count()
#         ret = super(Groupserializer, self).to_representation(instance)
#         ret["member"] = member
#         return ret
#
#
#     class Meta:
#         model = Group
#         fields = ("id", "name")