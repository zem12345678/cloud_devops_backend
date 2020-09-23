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


from paramiko.rsakey import RSAKey
import io
class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    username    = serializers.CharField(required=False, read_only=False, max_length=32, label="用户名", help_text="用户名")
    name        = serializers.CharField(required=False, read_only=False, label="姓名", help_text="姓名")
    is_active   = serializers.BooleanField(required=False, label="登陆状态", help_text="登陆状态")
    email       = serializers.CharField(read_only=True, help_text="联系邮箱")
    last_login  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="上次登录时间")
    phone       = serializers.CharField(required=False, max_length=11, min_length=11, allow_null=True, help_text="手机号",
                                        error_messages={"max_length":"手机号错误","min_length":"手机号错误"},
                                        )

    class Meta:
        model = UserProfile
        fields = ("id", "username", "name", "phone", "email", "is_active", "last_login")


# class UserRegSerializer(serializers.ModelSerializer):
#     """
#     用户注册序列化类
#     """
#     id       = serializers.IntegerField(read_only=True)
#     name     = serializers.CharField(max_length=32, label="姓名", help_text="用户姓名，中文姓名")
#     username = serializers.CharField(max_length=32, label="用户名", help_text="用户名，用户登陆名")
#     password = serializers.CharField(style={"input_type": "password"}, label="密码", write_only=True, help_text="密码")
#     phone    = serializers.CharField(max_length=11, min_length=11, label="手机号", required=False,
#                                      allow_null=True, allow_blank=True, help_text="手机号")
#
#     def create(self, validated_data):
#         validated_data["is_active"] = False
#         instance = super(UserRegSerializer, self).create(validated_data=validated_data)
#         instance.email = "{}{}".format(instance.username, settings.DOMAIN)
#
#         instance.set_password(validated_data["password"])
#         instance.id_rsa_key, instance.id_rsa_pub = self.get_sshkey(instance.email)
#         instance.save()
#         return instance
#
#     def update(self, instance, validated_data):
#         password =  validated_data.get("password", None)
#         if password:
#             instance.set_password(password)
#             instance.save()
#         return instance
#
#     def get_sshkey(self, email):
#         output = io.StringIO()
#         sbuffer = io.StringIO()
#
#         key = RSAKey.generate(2048)
#         key.write_private_key(output)
#         private_key = output.getvalue()
#
#         sbuffer.write("{} {} {}".format(key.get_name(), key.get_base64(), email))
#         public_key = sbuffer.getvalue()
#         return private_key, public_key
#
#     class Meta:
#         model = UserProfile
#         fields = ("username", "password", "name", "id", "phone")