# @Time    : 2020/9/19 19:39
# @Author  : ZhangEnmin
# @FileName: middleware.py
# @Software: PyCharm
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import requests
import json


class HttpResponseAuthenticationFailed(HttpResponse):
    status_code = 401


class TokenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path != "/docs/":
            try:
                # 子系统之间的验证
                app_key = request.headers["app-key"]
                app_name = request.headers["app-name"]
                if app_name and app_key:
                    data = {'app_key': app_key, 'app_name': app_name}
                    r = requests.post("http://101.200.61.189:8888/authper/", data=data)
                    if r.json()['status'] != 1:
                        return HttpResponseAuthenticationFailed(r.text)
                else:
                    # 去sso认证用户是否存在
                    Authorization = request.headers["Authorization"]
                    if Authorization:
                        headers = {"Authorization": Authorization}
                        r = requests.get("http://101.200.61.189:52131/userInfo/", headers=headers)
                        if r.status_code == 200:
                            request.user = r.json()
                        else:
                            content = {"detail": "User verification does not pass."}
                            return HttpResponseAuthenticationFailed(json.dumps(content))
            except:
                pass
                # content = {"detail": "Authentication credentials were not provided."}
                # return HttpResponseAuthenticationFailed(json.dumps(content))
