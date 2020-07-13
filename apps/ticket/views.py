from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import BasicTicketTemplate, TicketDetail 
from .serializers import BasicTicketTemplateSerializer, TicketDetailSerializer 





# 工单模板 
class TicketTemplateApiView(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 获取分类列表
    def get(self, request, *args, **kwargs):
        result = {
            "code": 20000,
            "message": "成功",
            "data": ""
        }
        retdata = {}
        for obj in BasicTicketTemplate.objects.all():
            ftitle, ttitle = obj.f_title, obj.t_title
            if ftitle not in retdata:
                retdata[ftitle] = [ttitle, ]
            else:
                retdata[ftitle].append(ttitle)

        result["data"] = retdata 
        return JsonResponse(result)



# 工单详情 
class TicketDetailViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回单个对象信息
    list:
        返回所有对象信息

    1. 用户提交过的历史工单 /api/v1/ticket/?creator=1
    2. 用户待处理的工单     /api/v1/ticket/?creator=1&status=1
    3. 用户处理完成的工单| 拒绝和处理完成 /api/v1/ticket/?creator=1&status=3
    '''
    queryset = TicketDetail.objects.all()
    serializer_class = TicketDetailSerializer 
    permission_classes = [] # 保留
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('creator', 'status')




@csrf_exempt   # 关闭csrf功能, 不需要csrf认证.
# @csrf_protect  # 打开csrf功能, 需要csrf认证.
def TicketDemoTestApi(request):
    return HttpResponse("TicketDemoTestApi")

