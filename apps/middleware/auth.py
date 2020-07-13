from rest_framework.permissions import BasePermission
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from apps.permission.models import ApiPermission


class AuthTokenRequired(BasePermission):
    """
        Token permission controller.
    """

    TOKEN = ""
    PATH = ""
    METHOD = ""

    def has_permission(self, request, view):

        metadata = request.META
        # 1. 验证Token是否传递。
        if not self.is_valid(metadata):
            return False

        # 2. 获取必要参数信息
        self.PATH = metadata.get("PATH_INFO", None)
        self.METHOD = metadata.get("REQUEST_METHOD", None)

        # 3. 认证
        if not self.auth():
            return False

        return True

    def is_valid(self, jwt_token):

        http_authorization = jwt_token.get("HTTP_AUTHORIZATION", None)
        if not http_authorization:
            print("key:Authorization not found from request.META")
            return False

        if not isinstance(http_authorization, str):
            return False

        authorization_array = http_authorization.split()
        if len(authorization_array) != 2:
            print("key:Authorization found, but value length is not valid")
            return False

        if "jwt" != authorization_array[0].lower():
            return False

        self.TOKEN = authorization_array[1]
        return True

    def auth(self):

        # Token得到用户名
        token_user = jwt_decode_handler(self.TOKEN)

        # 验证URI 和 Method
        try:
            ap = ApiPermission.objects.get(uri=self.PATH)
            method_list = [x.method for x in ap.api_http_methods.all()]
            groups = ap.api_permissions.all()
            users = []
            for g in groups:
                users.extend([u.username for u in g.users.all()])
            users = list(set(users))
            print("Users: {}.".format(users))
        except ApiPermission.DoesNotExist as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False

        print("path: {}, method: {}, username: {}.".format(self.PATH, self.METHOD, token_user))

        if self.METHOD not in method_list or token_user.get("username") not in users:
            return False

        return True
