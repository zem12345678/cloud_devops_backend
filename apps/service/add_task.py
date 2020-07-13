import json
import uuid
from apps.task import models
from utils.operating_redis import redis_object
from conf import TASK_WAITING
from service.master.core.state import WAITING


def add_task(task_id, targets):

    # {'task': {'task_id': 'task-2', 'script': 'mkdir ~/lanyulei_test'}, 'targets': ['5d8e2482156b4525b08f2367389c459b']}
    task_value = list(models.TaskList.objects.filter(id=task_id).values())
    task_params = {"targets": targets, "task": {"uuid": uuid.uuid1().hex}}
    if len(task_value) > 0:
        task_params["task"]["task_id"] = int(task_value[0].get("id", 0))
        task_params["task"]["script"] = task_value[0].get("content", "")
        redis_object.lpush(TASK_WAITING, json.dumps(task_params))
        for target in task_params["targets"]:
            models.TaskHistory.objects.create(**{
                "agent": target,
                "uuid": task_params["task"]["uuid"],
                "task_name": task_value[0].name,
                "status": WAITING
            })
