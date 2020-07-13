from django.views.generic import View
from django.http import  HttpResponse
from utils.gitlab_api import  get_user_projects, get_project_versions
import  json


class ProjectListView(View):
    """
    登陆用户所有项目列表
    """
    def get(self, request):
        my_projects = get_user_projects(request)
        json_list = []
        for project in my_projects:
            json_dict = {}
            json_dict['id'] = project.id
            json_dict['name'] = project.name
            json_dict['path_with_namespace'] = project.path_with_namespace
            json_dict['web_url'] = project.web_url
            json_dict['description'] = project.description
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list), content_type="application/json")


class ProjectVersionsView(View):
    """
    获取指定项目的所有版本
    """

    def get(self, request):
        project_id = request.GET.get('project_id')
        print(project_id)
        tags = get_project_versions(int(project_id))
        tags = [[tag.name, tag.message] for tag in tags]
        return HttpResponse(json.dumps(tags), content_type='application/json')








