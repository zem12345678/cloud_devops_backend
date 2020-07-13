from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.Serializer):
    """
    用户序列化类
    """
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, max_length=32, label="用户名", help_text="用户名")
    name = serializers.CharField(required=False, label="姓名", help_text="姓名")
    password = serializers.CharField(required=True, write_only=True, min_length=6, max_length=32, label="密码",
                                     help_text="密码")
    is_active = serializers.BooleanField(required=False, read_only=True, label="登陆状态", default=True, help_text="登陆状态")
    email = serializers.CharField(help_text="联系邮箱")
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="上次登录时间")
    phone = serializers.CharField(max_length=11, min_length=11, allow_null=True, help_text="手机号",
                                  error_messages={"max_length": "手机号错误", "min_length": "手机号错误"},
                                  )

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            return serializers.ValidationError("用户已存在")
        except User.DoesNotExist:
            return username

    def create(self, validated_data):
        validated_data["is_active"] = False
        instance = User()
        instance.username = validated_data["username"]
        instance.name = validated_data["name"]
        instance.phone = validated_data["phone"]
        instance.email = validated_data["email"]
        instance.is_active = True
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data.get("phone", None):
            instance.phone = validated_data["phone"]
        if validated_data.get("password", None):
            instance.set_password(validated_data["password"])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("id", "username", "name", "phone", "email", "is_active", "last_login", "password")
