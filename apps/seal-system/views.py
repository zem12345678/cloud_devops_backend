import logging
import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from system.models import Users
from django.urls import reverse_lazy
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from system.form import UserPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics

logger = logging.getLogger('system')


class UserInfo(APIView):
    """
    获取用户信息
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = (json.loads(request.body))['token']
        obj = Token.objects.get(key=token).user
        result = {
            'name': obj.username,
            'user_id': obj.id,
            'access': list(obj.get_all_permissions()) + ['admin'] if obj.is_superuser else list(
                obj.get_all_permissions()),
            'token': token,
            'avatar': 'https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png'
        }
        return HttpResponse(json.dumps(result))


class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = (json.loads(request.body))['token']
        obj = Token.objects.get(key=token)
        obj.delete()
        result = {
            "status": True
        }
        return HttpResponse(json.dumps(result))


class Menu(APIView):

    def post(self, request):
        result = [

            {
                "path": '/assets',
                "name": 'assets',
                "meta": {
                    "icon": 'md-menu',
                    "title": '资产管理'
                },
                "component": 'Main',
                "children": [
                    {
                        'path': 'ecs',
                        'name': 'ecs',
                        'meta': {
                            'access': ['assets.view_ecs'],
                            'icon': 'md-funnel',
                            'title': 'ecs'
                        },
                        'component': 'assets/ecs/ecs-list'
                    }
                ]
            },
            # {
            #     "path": '/multilevel',
            #     "name": 'multilevel',
            #     "meta": {
            #         "icon": 'md-menu',
            #         "title": '多级菜单'
            #     },
            #     "component": 'Main',
            #     "children": [
            #         {
            #             "path": '/level_2_1',
            #             "name": 'level_2_1',
            #             "meta": {
            #                 "icon": 'md-funnel',
            #                 "title": '二级-1'
            #             },
            #             "component": 'multilevel/level-2-1'
            #         },
            #
            #     ]
            # },
            {
                "path": '/k8s',
                "name": 'k8s',
                "meta": {
                    "icon": 'md-menu',
                    "title": '多级菜单'
                },
                "component": 'Main',
                "children": [
                    {
                        "path": '/pods',
                        "name": 'pods',
                        "meta": {
                            "icon": 'md-funnel',
                            "title": 'pods',
                        },
                        "component": 'k8s/k8s-pods'
                    },
                    {
                        "path": '/webssh/:name/:namespace',
                        "name": 'webssh',
                        "meta": {
                            "icon": 'md-funnel',
                            "title": 'webssh',
                            "hideInMenu": "true",
                        },
                        "component": 'k8s/k8s-webssh'
                    }

                ]
            }
        ]
        return HttpResponse(json.dumps(result))


class CustomBackend(ModelBackend):
    """
    用户名字/邮箱名字 登录
    :param request:
    :return:
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            logger.error(e)
            return None


def login_view(request):
    """
    登录
    :param request: username,password
    :return:
    """

    error_msg = "用户名或密码错误,或者被禁用,请重试"

    if request.method == "GET":
        return render(request, 'system/login.html', {'error_msg': error_msg, })

    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['is_login'] = True
                login_ip = request.META['REMOTE_ADDR']
                return redirect('/index')
            else:
                return render(request, 'system/login.html', {'error_msg': error_msg, })
        else:
            return render(request, 'system/login.html', {'error_msg': error_msg, })


@login_required(login_url="/system/login")
def index(request):
    """
    首页
    :param request:
    :return:
    """
    return render(request, 'system/index.html')


class UserPasswordUpdateView(LoginRequiredMixin, UpdateView):
    """
    修改密码
    :param request:
    :return:
    """
    template_name = 'system/password.html'
    model = Users
    form_class = UserPasswordForm
    success_url = reverse_lazy('system:logout')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return super().get_success_url()


def logout_view(request):
    """
    注销
    :param request:
    :return:
    """
    logout(request)
    return redirect('system:login')


class DisableCSRFCheck(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
