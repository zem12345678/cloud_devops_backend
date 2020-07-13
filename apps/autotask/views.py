import json
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.ansible_api import ANSRunner


from .serializers import TasksSerializer
from .models import Tasks


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class TasksViewset(viewsets.ModelViewSet):
    """
    create:
    创建任务
    list:
    获取热么列表
    retrieve:
    获取任务信息
    update:
    执行任务
    """
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)

    def partial_update(self, request, *args, **kwargs):
         pk = int(kwargs.get("pk"))
         data = request.data
         task = Tasks.objects.get(pk=pk)
         rbt = ANSRunner()
         print(task.playbook.path)
         rbt.run_playbook(task.playbook.path)
         data['detail_result'] = json.dumps(rbt.get_playbook_result(),indent=4)

         Tasks.objects.filter(pk=pk).update(**data)
         return Response(status=status.HTTP_204_NO_CONTENT)

