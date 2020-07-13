import gitlab

from cloud_devops_backend.settings import GITLAB_HTTP_URI, GITLAB_TOKEN
gl = gitlab.Gitlab(GITLAB_HTTP_URI, GITLAB_TOKEN,api_version="4")


def get_user_projects(request):
    """
    获取gitlab里所有的项目，和登录用户所拥有的项目,以及登录用户所拥有项目的项目成员
    :return: []
    """
    user_projects = []
    all_projects = gl.projects.list()
    print(request.user.username)
    # print(all_projects)


    # 获取当前用户所有的项目
    for project in all_projects:
        print(project)
        for member in project.members.list():
            # if member.username == request.user.username:
            if member.username == "ada":
                user_projects.append(project)
    # print(user_projects)
    return user_projects


def get_project_versions(project_id):
    """
    获取某个项目的版本号
    :param project_id:
    :return:
    """
    project = gl.projects.get(project_id)
    tags = project.tags.list()
    print(tags)
    return tags

