from rest_framework.views import APIView
from cmdb import models
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from cloud_devops_backend.basic import OpsResponse
from cloud_devops_backend.code import *

class Classification(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 获取分类列表
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
        name = request.GET.get("name", "")
        if name == "":
            value_list = list(models.Classification.objects.all().order_by("-id").values()[(page - 1) * 10: limit * page])
        else:
            value_list = list(
                models.Classification.objects.filter(name__icontains=name).order_by("-id").values()[(page - 1) * 10: limit * page])

        res = {
            "list": value_list,
            "total": models.Classification.objects.count()
        }
        return OpsResponse(res,status=OK)

    # 新建分类
    def post(self, request, *args, **kwargs):
        value = {
            "name": request.data.get("name"),
            "remarks": request.data.get("remarks")
        }
        try:
            models.Classification.objects.create(**value)
        except Exception as e:
            return OpsResponse("新建分类失败，{}".format(e),status=BAD)
        return OpsResponse("新建分类成功")

    # 修改分类
    def put(self, request, *args, **kwargs):
        value = {
            "name": request.data.get("name"),
            "remarks": request.data.get("remarks")
        }

        try:
            models.Classification.objects.filter(id=request.data.get("id", 0)).update(**value)
        except Exception as e:
             return OpsResponse("修改分类失败，{}".format(e),status=BAD)
        return OpsResponse("修改分类成功")

    # 删除分类
    def delete(self, request, *args, **kwargs):
        id = request.data.get("id", 0)
        try:
            models.Classification.objects.filter(id=id).delete()
        except Exception as e:
            return OpsResponse("删除分类失败，{}".format(e),status=BAD)
        return OpsResponse("删除分类成功")


class Table(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 表列表
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
        name = request.GET.get("name", "")
        try:
            if name == "":
                value_list = list(models.Table.objects.all().order_by("-id").values()[(page - 1) * 10: limit * page])
            else:
                value_list = list(
                    models.Table.objects.filter(name__icontains=name).order_by("-id").values()[(page - 1) * 10: limit * page])
            for table_value in value_list:
                classification_value = models.Classification.objects.filter(id=table_value.get("classification_id", 0))
                if classification_value:
                    table_value["classification_name"] = classification_value[0].name
                else:
                    table_value["classification_name"] = None

                table_value["classification"] = table_value["classification_id"]

            result_list = {
                "list": value_list,
                "total": models.Table.objects.count()
            }
        except Exception as e:
            return OpsResponse("获取表数据失败，{}".format(e),status=BAD)
        return OpsResponse(result_list)

    # 新建表
    def post(self, request, *args, **kwargs):
        try:
            table_value = request.data
            classification_obj = models.Classification.objects.get(id=table_value.get("classification", 0))
            table_value["classification"] = classification_obj
            models.Table.objects.create(**table_value)
        except Exception as e:
            return OpsResponse("新建表失败，{}".format(e), status=BAD)
        return OpsResponse("新建表成功")

    # 更新表
    def put(self, request, *args, **kwargs):
        try:
            table_value = {
                "name": request.data.get("name"),
                "alias": request.data.get("alias"),
                "classification": models.Classification.objects.get(id=request.data.get("classification")),
                "fields": request.data.get("fields"),
                "remarks": request.data.get("remarks")
            }
            models.Table.objects.filter(id=request.data.get("id")).update(**table_value)
        except Exception as e:
            return OpsResponse("更新表失败，{}".format(e), status=BAD)
        return OpsResponse("更新表成功")

    # 删除表
    def delete(self, request, *args, **kwargs):
        id = request.data.get("id", 0)
        try:
            models.Table.objects.filter(id=id).delete()
        except Exception as e:
            return OpsResponse("删除表失败，{}".format(e),status=BAD)
        return OpsResponse("删除表成功")


class ClassificationTable(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 获取类型对应的表
    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get("id")
            table_list = list(models.Table.objects.filter(classification=id).values("id", "name", "alias"))
            res= table_list
        except Exception as e:
            return OpsResponse(f"获取表数据失败，{e}",status=BAD)
        return OpsResponse(res)


class TableValue(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 获取类型对应的表
    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get("id")
            table_value = list(models.Table.objects.filter(id=id).values())[0]
        except Exception as e:
            return OpsResponse(f"获取表数据失败，{e}",status=BAD)
        return OpsResponse(table_value)


class Data(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 数据列表
    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            table_id = int(request.GET.get("table_id", 0))
            search_key = request.GET.get("searchKey", "")
            search_value = request.GET.get("searchValue", "")
            table_object = models.Table.objects.get(id=table_id)
            if search_key == "" or search_value == "":
                value_list = list(models.Data.objects.filter(table=table_object).
                                  order_by("-id").values()[(page - 1) * 10: limit * page])
            else:
                value_list = list(models.Data.objects.filter(table=table_object).
                                  extra(
                    where=[f'''json_extract(value,  '$.{search_key}' ) like "%%{search_value}%%"''']).
                                  order_by("-id").values()[(page - 1) * 10: limit * page])
            result_list = {
                "list": value_list,
                "total": models.Data.objects.filter(table_id=table_id).count()
            }
        except Exception as e:
            return OpsResponse(f"获取表数据失败，{e}", status=BAD)
        return OpsResponse(result_list)

    # 新建数据
    def post(self, request, *args, **kwargs):
        try:
            data_value = {
                "table": models.Table.objects.get(id=request.data.get("table", 0)),
                "value": request.data.get("value")
            }
            models.Data.objects.create(**data_value)
        except Exception as e:
            return OpsResponse(f"创建数据失败，{e}",status=BAD)
        return OpsResponse("创建数据成功")

    # 编辑数据
    def put(self, request, *args, **kwargs):
        try:
            data_id = int(request.data.get("data_id", 0))
            data_value = {
                "table": models.Table.objects.get(id=request.data.get("table", 0)),
                "value": request.data.get("value")
            }

            models.Data.objects.filter(id=data_id).update(**data_value)
        except Exception as e:
            return OpsResponse(f"更新数据失败，{e}",status=BAD)
        return OpsResponse("更新数据成功")

    # 删除数据
    def delete(self, request, *args, **kwargs):
        try:
            data_id = request.data.get("data_id", 0)
            models.Data.objects.filter(id=data_id).delete()
        except Exception as e:
            return OpsResponse( f"删除数据失败，{e}",status=BAD)
        return OpsResponse("删除数据成功")