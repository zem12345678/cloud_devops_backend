import json
import uuid
from apps.task import models
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from conf import TASK_WAITING
from utils.operating_redis import redis_object
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from service.add_task import add_task
from service.master.core.state import WAITING


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore())
scheduler.start()


class TaskList(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ 任务列表 """

        result = {"code": 20000, "message": "成功"}
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            result["data"] = {
                "list": list(models.TaskList.objects.all().values())[(page - 1) * 10 : limit * page],
                "total": models.TaskList.objects.count(),
            }
        except Exception as e:
            result["code"] = 400
            result["message"] = f"获取任务列表失败，{e}"

        return JsonResponse(result)

    def post(self, request, *args, **kwargs):
        """ 新建或者任务 """

        result = {"code": 20000, "message": "成功"}
        try:
            task_id = int(request.data.get("id", 0))
            if task_id == 0:
                models.TaskList.objects.create(**request.data)
            else:
                models.TaskList.objects.filter(id=task_id).update(**request.data)
        except Exception as e:
            result["code"] = 400
            result["message"] = f"新建任务失败，{e}"

        return JsonResponse(result)

    def delete(self, request, *args, **kwargs):
        """ 新建任务 """

        result = {"code": 20000, "message": "成功"}
        try:
            models.TaskList.objects.filter(id=request.data.get("id", 0)).delete()
        except Exception as e:
            result["code"] = 400
            result["message"] = f"删除任务失败，{e}"

        return JsonResponse(result)


class ExecuteTask(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """ 加入执行队列 """

        result = {"code": 20000, "message": "成功"}
        try:
            params = request.data
            params["targets"] = list(set(params["targets"]))
            params["task"]["uuid"] = uuid.uuid1().hex

            task = models.TaskList.objects.get(id=params["task"]["task_id"])

            redis_object.lpush(TASK_WAITING, json.dumps(params))
            for target in params["targets"]:
                models.TaskHistory.objects.create(
                    **{"agent": target, "uuid": params["task"]["uuid"], "task_name": task.name, "status": WAITING}
                )
        except Exception as e:
            result["code"] = 400
            result["message"] = f"执行失败，{e}"

        return JsonResponse(result)


class ScheduledTask(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ 任务列表 """

        result = {"code": 20000, "message": "成功"}
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            task_all_list = scheduler.get_jobs()
            result["data"] = {"list": [], "total": len(task_all_list)}
            for task in task_all_list[(page - 1) * 10 : limit * page]:
                try:
                    task_obj = models.TaskList.objects.get(id=task.args[0])
                    result["data"]["list"].append(
                        {"id": task.id, "task_name": task_obj.name, "next_run_time": task.next_run_time}
                    )
                except Exception as e:
                    print(e)
        except Exception as e:
            result["code"] = 400
            result["message"] = f"执行失败，{e}"

        return JsonResponse(result)

    def post(self, request, *args, **kwargs):
        """ 新建定时任务 """

        result = {"code": 20000, "message": "成功"}
        try:
            execution_way = request.data.get("execution_way")
            execution_way = execution_way.split()
            if len(execution_way) != 5:
                result["code"] = 400
                result["message"] = "执行执行类型错误，请确认是否有六组数据"
            else:
                year = execution_way[0]
                month = execution_way[1]
                day = execution_way[2]
                hour = execution_way[3]
                minute = execution_way[4]
                # 添加任务
                scheduler.add_job(
                    add_task,
                    "cron",
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=1,
                    args=[request.data.get("task_id", 0), list(set(request.data.get("targets", [])))],
                )
                # 注册任务
                register_events(scheduler)
        except Exception as e:
            import traceback

            traceback.print_exc()
            result["code"] = 400
            result["message"] = f"新建定时任务失败，{e}"

        return JsonResponse(result)

    def delete(self, request, *args, **kwargs):
        """ 删除定时任务 """

        result = {"code": 20000, "message": "成功"}
        try:
            scheduler.remove_job(request.data.get("job_id", ""))
        except Exception as e:
            result["code"] = 400
            result["message"] = f"获取任务列表失败，{e}"

        return JsonResponse(result)

    def put(self, request, *args, **kwargs):
        """ 修改定时任务状态 """

        result = {"code": 20000, "message": "成功"}
        try:
            job_id = request.data.get("job_id", "")
            status = int(request.data.get("status", -1))
            if status == 1:
                scheduler.resume_job(job_id)
            elif status == 0:
                scheduler.pause_job(job_id)

        except Exception as e:
            result["code"] = 400
            result["message"] = f"获取任务列表失败，{e}"

        return JsonResponse(result)


class TaskHistory(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        result = {"code": 20000, "message": "成功"}
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            history_list = list(
                models.TaskHistory.objects.all().values(
                    "agent", "uuid", "task_name", "status", "start_time", "end_time"
                )
            )[(page - 1) * 10 : limit * page]

            result["data"] = {"list": history_list, "total": models.TaskHistory.objects.count()}
        except Exception as e:
            result["code"] = 400
            result["message"] = f"删除任务失败，{e}"

        return JsonResponse(result)


class TaskHistoryDetails(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        result = {"code": 20000, "message": "成功"}
        try:
            result["data"] = list(
                models.TaskHistory.objects.filter(
                    agent=request.GET.get("agent", ""), uuid=request.GET.get("uuid", "")
                ).values("content")
            )[0]["content"]
        except Exception as e:
            result["code"] = 400
            result["message"] = f"获取任务历史列表失败，{e}"

        return JsonResponse(result)
