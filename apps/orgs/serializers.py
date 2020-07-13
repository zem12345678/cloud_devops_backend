from django.contrib.auth import get_user_model
from .models import Organization
from pms.models import Permission
from rest_framework import serializers
import django.utils.timezone as timezone
User = get_user_model()


class GroupMembersSerizlizer(serializers.Serializer):
    uids = serializers.ListField(required=True)

    def validate_uids(self, uids):
        userIds = []
        objs = User.objects.filter(pk__in=uids)
        for obj in objs:
            userIds.append(str(obj.id))
        if userIds != uids:
            raise serializers.ValidationError("uid 错误")
        return objs


class GroupPermissionSerizlizer(serializers.Serializer):
    pids = serializers.ListField(required=True)

    def validate_uids(self, pids):
        perIds = []
        objs = Permission.objects.filter(pk__in=pids)
        for obj in objs:
            perIds.append(str(obj.id))
        if perIds != pids:
            raise serializers.ValidationError("pid 错误")
        return objs


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
        member = self.get_users(instance.users.all())
        ret = super(GroupSerializer, self).to_representation(instance)
        ret["nodes"] = nodes
        ret["permissions"] = permissions
        ret["member"] = member
        return ret

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return Organization.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.created_by = validated_data.get('created_by', str(self.context['request'].user))
        instance.save()
        return instance

    class Meta:
        model = Organization
        fields = ("id", "name", "comment", 'created_by', 'date_created')
        read_only_fields = ('created_by', 'date_created')
