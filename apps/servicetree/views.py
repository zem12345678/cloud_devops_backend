from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from cmdb import models as cmdb_models
from django.db import connection, transaction
from .models import Node,ServiceTree,BindCMDB
from .serializers import NodeSerializer
from cloud_devops_backend.basic import OpsResponse
from cloud_devops_backend.code import *


class NodeViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    retrieve:
    返回指定Node信息
    update:
    更新Node信息
    destroy:
    删除Node记录
    create:
    创建Node资源
    partial_update:
    更新部分字段
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer



class ServiceTreeViewSet(viewsets.GenericViewSet):
    """
    list:
    返回所有服务树列表信息
    """

    def list(self, request, *args, **kwargs):
        data = self.get_tree()
        return data

    def get_tree(self):
        return self.get_child_node(0)

    def get_child_node(self, pid):
        ret = []
        for obj in Node.objects.filter(pid__exact=pid):
            node = self.get_node(obj)
            node["children"] = self.get_child_node(obj.id)
            ret.append(node)
        return OpsResponse(ret,status=OK)

    def get_node(self, obj):
        node = {}
        node["id"] = obj.id
        node["label"] = obj.name
        node["pid"] = obj.pid
        return node



class ServiceTree(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 获取树状结构数据
    def get(self, request, *args, **kwargs):

        result = {"code": 20000, "message": "成功", "data": ""}

        # 递归函数
        def set_children(id, menus):
            """
            根据传递过来的父菜单id，递归设置各层次父菜单的子菜单列表

            :param id: 父级id
            :param menus: 子菜单列表
            :return: 如果这个菜单没有子菜单，返回None;如果有子菜单，返回子菜单列表
            """
            # 记录子菜单列表
            children = []
            # 遍历子菜单
            for m in menus:
                if m["parent"] == id:
                    children.append(m)

            # 把子菜单的子菜单再循环一遍
            for sub in children:
                menus2 = list(
                    ServiceTree.objects.filter(parent=sub["id"]).values("id", "label", "parent", "level")
                )
                # 还有子菜单
                if len(menus):
                    children_value = set_children(sub["id"], menus2)
                    if children_value is not None:
                        sub["children"] = children_value

            # 子菜单列表不为空
            if len(children):
                return children
            else:  # 没有子菜单了
                return None

        # 一级菜单
        top_menus = list(ServiceTree.objects.filter(parent=0).values("id", "label", "parent", "level"))
        for menu in top_menus:
            children = list(
                ServiceTree.objects.filter(parent=menu["id"]).values("id", "label", "parent", "level")
            )
            menu["children"] = set_children(menu["id"], children)

        result["data"] = top_menus

        return JsonResponse(result)

    # 创建节点数据
    def post(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": ""}
        try:
            data = {
                "label": request.data.get("label"),
                "parent": request.data.get("parent"),
                "level": request.data.get("level"),
            }
            ServiceTree.objects.create(**data)
        except Exception as e:
            result["code"] = 400
            result["message"] = f"创建节点数据，{e}"

        return JsonResponse(result)

    # 编辑节点数据
    def put(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": ""}
        try:
            ServiceTree.objects.filter(id=request.data.get("id")).update(**{"label": request.data.get("label")})
        except Exception as e:
            result["code"] = 400
            result["message"] = f"创建节点数据，{e}"

        return JsonResponse(result)

    # 删除节点数据
    def delete(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": ""}
        try:
            ServiceTree.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            result["code"] = 400
            result["message"] = f"创建节点数据，{e}"

        return JsonResponse(result)


class BindCMDBData(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 绑定数据
    def post(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": ""}
        try:
            dataCount = BindCMDB.objects.filter(
                service_tree=request.data.get("service_tree", 0),
                classification=request.data.get("classification", 0),
                table=request.data.get("table", 0),
                data=request.data.get("data", 0),
            ).count()
            if dataCount == 0:
                BindCMDB.objects.create(**request.data)
            else:
                BindCMDB.objects.filter(
                    service_tree=request.data.get("service_tree", 0),
                    classification=request.data.get("classification", 0),
                    table=request.data.get("table", 0),
                    data=request.data.get("data", 0),
                ).delete()
        except Exception as e:
            result["code"] = 400
            result["message"] = e

        return JsonResponse(result)

    # 解除绑定
    def delete(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": ""}

        try:
            bind_id = request.data.get("bind_id", 0)
            BindCMDB.objects.filter(id=bind_id).delete()
        except Exception as e:
            result["code"] = 400
            result["message"] = e
        return JsonResponse(result)


class ServiceTreeCMDB(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 初始化数据
    def get(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": {"classification": [], "table": [], "data": {}}}

        try:
            service_tree_id = request.GET.get("service_tree_id", 0)
            classification_id = int(request.GET.get("classification_id", 0))
            if service_tree_id == 0:
                result["code"] = 400
                result["message"] = "service_tree_id参数未传递"
            else:
                # 获取所有绑定的分类
                classification_id_list = set()
                data_fields_list = []
                classification_list = list(
                    BindCMDB.objects.filter(service_tree=service_tree_id).values_list("classification")
                )
                if len(classification_list) > 0:
                    for classification in classification_list:
                        classification_id_list.add(classification[0])
                    classification_id_list = sorted(list(classification_id_list))
                    result["data"]["classification"] = list(
                        cmdb_models.Classification.objects.filter(id__in=classification_id_list).values("id", "name")
                    )

                    # 获取绑定的分类对应的表
                    if classification_id == 0:
                        classification_id = classification_id_list[0]
                    table_id_list = set()
                    table_list = list(
                        BindCMDB.objects.filter(
                            classification=classification_id, service_tree=service_tree_id
                        ).values_list("table")
                    )
                    if len(table_list) > 0:
                        for table in table_list:
                            table_id_list.add(table[0])
                        table_id_list = sorted(list(table_id_list))
                        result["data"]["table"] = list(
                            cmdb_models.Table.objects.filter(id__in=table_id_list).values(
                                "id", "name", "alias", "fields"
                            )
                        )

                        # 获取表对应的数据
                        data_id_list = list(
                            BindCMDB.objects.filter(
                                service_tree=service_tree_id,
                                classification=classification_id,
                                table=table_id_list[0],
                            ).values_list("id", "data")
                        )
                        data_id_list_tmp = [i[1] for i in data_id_list]

                        data_list = list(
                            cmdb_models.Data.objects.filter(id__in=data_id_list_tmp).values("id", "table_id", "value")[
                                0:10
                            ]
                        )
                        if len(data_list) > 0:
                            for data_value in data_list:
                                bind_id = [i[0] for i in data_id_list if i[1] == data_value["id"]]
                                data_fields_dict = {
                                    "bind_id": bind_id[0],
                                    "id": data_value["id"],
                                    "table_id": data_value["table_id"],
                                }
                                data_fields_dict.update(data_value["value"])
                                data_fields_list.append(data_fields_dict)
                        result["data"]["data"] = {
                            "list": data_fields_list,
                            "total": cmdb_models.Data.objects.filter(id__in=data_id_list_tmp).count(),
                        }

        except Exception as e:
            result["code"] = 400
            result["message"] = e
            import traceback

            traceback.print_exc()
        return JsonResponse(result)


class ServiceTreeCMDBTable(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": ""}
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            data_id_list = list(
                BindCMDB.objects.filter(
                    service_tree=request.GET.get("service_tree", 0),
                    classification=request.GET.get("classification", 0),
                    table=request.GET.get("table"),
                ).values_list("id", "data")
            )
            data_id_list_tmp = [i[1] for i in data_id_list]

            data_fields_list = []
            data_list = list(
                cmdb_models.Data.objects.filter(id__in=data_id_list_tmp).values("id", "table_id", "value")[
                    (page - 1) * 10 : limit * page
                ]
            )
            if len(data_list) > 0:
                for data_value in data_list:
                    bind_id = [i[0] for i in data_id_list if i[1] == data_value["id"]]
                    data_fields_dict = {
                        "bind_id": bind_id[0],
                        "id": data_value["id"],
                        "table_id": data_value["table_id"],
                    }
                    data_fields_dict.update(data_value["value"])
                    data_fields_list.append(data_fields_dict)

            result["data"] = {
                "list": data_fields_list,
                "total": cmdb_models.Data.objects.filter(id__in=data_id_list_tmp).count(),
            }

        except Exception as e:
            result["code"] = 400
            result["message"] = e
        return JsonResponse(result)


class ServiceTreeNotCMDB(APIView):
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 获取服务树未对应的cmdb数据
    def get(self, request, *args, **kwargs):
        result = {"code": 20000, "message": "成功", "data": {"list": [], "total": 0}}
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            service_tree = int(request.GET.get("service_tree", 0))
            classification = int(request.GET.get("classification", 0))
            table = int(request.GET.get("table", 0))
            rows_sql = """select %s from cmdb_data where id not in (select data from service_tree_cmdb 
                where service_tree_cmdb.service_tree = {service_tree}
                    and service_tree_cmdb.classification = {classification}
                    and service_tree_cmdb.`table` = {table_id}) 
                    and table_id = {table_id} limit {limit} offset %s;""".format(
                service_tree=service_tree,
                classification=classification,
                table_id=table,
                limit=limit,
                page=(page - 1) * limit,
            )
            # list
            rows = cmdb_models.Data.objects.raw(rows_sql % ("*", (page - 1) * limit))
            if len(rows) > 0:
                for row in rows:
                    result["data"]["list"].append({"id": row.id, "value": row.value, "table_id": row.table.id})

                # total
                cursor = connection.cursor()
                print(rows_sql % ("count(cmdb_data.id)", "0"))
                cursor.execute(rows_sql % ("count(cmdb_data.id)", "0"))
                raw_count = cursor.fetchone()
                print(raw_count)
                result["data"]["total"] = raw_count[0]

        except Exception as e:
            result["code"] = 400
            result["message"] = e
            import traceback

            traceback.print_exc()
        return JsonResponse(result)
