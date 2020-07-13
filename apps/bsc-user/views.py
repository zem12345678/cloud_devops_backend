from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.user.models import UserProfile
from django.http import JsonResponse

from apps.middleware.auth import AuthTokenRequired


result = {
    "code": 20000,
    "message": "成功",
    "data": ""
}


class UserInfo(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result["data"] = list(UserProfile.objects.filter(username=request.user).values())[0]
        return JsonResponse(result)


class TestApiPermission(APIView):
    permission_classes = [AuthTokenRequired, ]

    def get(self, request, *args, **kwargs):
        return JsonResponse(result)
