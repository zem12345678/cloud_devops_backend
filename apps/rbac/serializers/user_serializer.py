# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm
from rest_framework import serializers
from ..models import UserProfile
import re


class UserListSerializer(serializers.ModelSerializer):
    '''
    用户列表的序列化
    '''
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'image', 'department', 'position', 'superior',
                  'is_active','roles']
        depth = 1


class UserModifySerializer(serializers.ModelSerializer):
    '''
    用户编辑的序列化
    '''
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'image', 'department', 'position', 'superior',
                  'is_active', 'roles']

    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        return mobile

    # def update(self, instance, validated_data):
    #     if validated_data.get("phone", None):
    #         instance.phone = validated_data["phone"]
    #     if validated_data.get("password", None):
    #         instance.set_password(validated_data["password"])
    #     instance.save()
    #     return instance


class UserCreateSerializer(serializers.ModelSerializer):
    '''
    创建用户序列化
    '''
    username = serializers.CharField(required=True, allow_blank=False)
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'department', 'position', 'is_active', 'roles',
                  'password']

    def validate_username(self, username):
        if UserProfile.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError("手机号已经被注册")
        return mobile

    # def create(self, validated_data):
    #     validated_data["is_active"] = False
    #     instance = UserProfile()
    #     instance.username = validated_data["username"]
    #     instance.name = validated_data["name"]
    #     instance.phone = validated_data["phone"]
    #     instance.email = validated_data["email"]
    #     instance.is_active = True
    #     instance.set_password(validated_data["password"])
    #     instance.save()
    #     return instance

class UserInfoListSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    class Meta:
        model = UserProfile
        fields = ('id','name','mobile','email','position')