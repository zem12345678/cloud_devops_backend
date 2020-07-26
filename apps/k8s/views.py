import logging
from rest_framework import viewsets
from rest_framework import mixins
from k8s.k8sApi.core import K8sApi
from cloud_devops_backend.basic import OpsResponse

logger = logging.getLogger('k8s')



class K8sNodeListView(viewsets.GenericViewSet,mixins.ListModelMixin):
    permission_required = ('k8s.view_ecs',)

    def list(self, request, *args, **kwargs):
        obj = K8sApi()
        ret = obj.get_node_list()
        data = {}
        for i in ret.items:
            data[i.metadata.name] = {"name": i.metadata.name,
                                     "status": i.status.conditions[-1].type if i.status.conditions[ -1].status == "True" else "NotReady",
                                     "ip": i.status.addresses[0].address,
                                     "kubelet_version": i.status.node_info.kubelet_version,
                                     "os_image": i.status.node_info.os_image,
                                     }
        return OpsResponse(data=data)


class K8sServiceListView(viewsets.GenericViewSet,mixins.ListModelMixin):
    permission_required = ('k8s.view_ecs',)

    def list(self, request, *args, **kwargs):
        obj = K8sApi()
        ret = obj.get_service_list()
        data = {}
        for i in ret.items:
            print(i)
            ports = []
            for j in i.spec.ports:
                ports.append(f"{j.target_port}/{j.port}/{j.node_port}")
            data[i.metadata.name] = {"name": i.metadata.name, "cluster_ip": i.spec.cluster_ip, "type": i.spec.type,
                                     "external_i_ps": i.spec.external_i_ps,
                                     "port": ports}
        return OpsResponse(data=data)



class K8sPodListView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    permission_required = ('k8s.view_ecs',)

    def list(self, request, *args, **kwargs):
        obj = K8sApi()
        ret = obj.get_pod_list()
        data = {}
        for i in ret.items:
            data[i.metadata.name] = {"ip": i.status.pod_ip, "namespace": i.metadata.namespace}
        return OpsResponse(data=data)

    def retrieve(self, request, *args, **kwargs):
        name = self.request.GET.get("name")
        namespace = self.request.GET.get("namespace")
        obj = K8sApi()
        data = obj.get_pod_detail(name, namespace)
        return OpsResponse(data={"name": name, "namespace": namespace, "data": data})



class K8sPodWebSsh(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    permission_required = ('k8s.view_ecs',)

    def retrieve(self, request, *args, **kwargs):
        name = self.request.GET.get("name")
        namespace = self.request.GET.get("namespace")
        return OpsResponse(data={"name": name, "namespace": namespace})


# class K8sPodDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = ('k8s.view_ecs',)
#
#     def get(self, request):
#         name = self.request.GET.get("name")
#         namespace = self.request.GET.get("namespace")
#         obj = K8sApi()
#         data = obj.get_pod_detail(name, namespace)
#         return render(request, "k8s/k8s-pod-detail.html", {"name": name, "namespace": namespace, "data": data})
