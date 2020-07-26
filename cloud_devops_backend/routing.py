# @Time    : 2020/7/12 14:26
# @Author  : ZhangEnmin
# @FileName: routing.py
# @Software: PyCharm

from webSocket.jwt_auth import TokenAuthMiddleware
from channels.routing import URLRouter, ProtocolTypeRouter
from django.urls import path
from webSocket.consumers.console import ConsoleMsgConsumer

application = ProtocolTypeRouter({
    "webSocket": TokenAuthMiddleware(
        URLRouter([
            path(r"webSocket/console", ConsoleMsgConsumer),
        ])
    )
})