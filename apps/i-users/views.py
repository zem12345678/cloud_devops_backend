from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from .filters import UserFilter

User = get_user_model()


class UserInfoViewset(viewsets.ViewSet):
    """
    获取当前登陆的用户信息
    """
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
        }
        return Response(data)

class UsersViewset(viewsets.ModelViewSet):
    """
    create:
    添加用户
    retrieve:
    获取用户信息
    list:
    获取用户列表
    update:
    更新用户信息
    partial_update:
    更新用户信息
    delete:
    删除用户
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_fields = ("username",)