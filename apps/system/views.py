from apps.system import models
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RegisterApply(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ Agent注册审批 """

        result = {"code": 20000, "message": "成功"}
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            result["data"] = {
                "list": list(models.AgentApprovalList.objects.all().values())[(page - 1) * 10 : limit * page],
                "total": models.AgentApprovalList.objects.count(),
            }
        except Exception as e:
            result["code"] = 400
            result["message"] = f"获取agent注册审批失败，{e}"

        return JsonResponse(result)

    def post(self, request, *args, **kwargs):
        """ 同意agent注册 """

        result = {"code": 20000, "message": "成功"}
        try:
            agent_id = request.data.get("agent_id")
            agent_values = list(
                models.AgentApprovalList.objects.filter(agent_id=agent_id).values(
                    "agent_id", "ipaddress", "hostname", "apply_time"
                )
            )[0]
            agent_count = models.AgentList.objects.filter(agent_id=agent_id).count()
            if agent_count == 0:
                models.AgentList.objects.create(**agent_values)
                agent_count = models.AgentList.objects.filter(agent_id=agent_id).count()
                if agent_count != 0:
                    models.AgentApprovalList.objects.filter(agent_id=agent_id).delete()

        except Exception as e:
            result["code"] = 400
            result["message"] = f"注册失败，{e}"

        return JsonResponse(result)


class AgentList(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ agent 列表 """

        result = {"code": 20000, "message": "成功"}
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            result["data"] = {
                "list": list(models.AgentList.objects.all().values())[(page - 1) * 10 : limit * page],
                "total": models.AgentList.objects.count(),
            }

        except Exception as e:
            result["code"] = 400
            result["message"] = f"获取agent列表失败，{e}"

        return JsonResponse(result)

    def delete(self, request, *args, **kwargs):
        """ 删除agent """

        result = {"code": 20000, "message": "成功"}
        try:
            models.AgentList.objects.filter(id=request.data.get("id")).delete()
        except Exception as e:
            result["code"] = 400
            result["message"] = f"删除Agent失败，{e}"

        return JsonResponse(result)


class IgnoreAgent(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 忽略agent注册
    def get(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功"}
        try:
            models.AgentApprovalList.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            result["code"] = 400
            result["message"] = f"忽略agent注册失败，{e}"

        return JsonResponse(result)
