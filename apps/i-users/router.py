from rest_framework.routers import DefaultRouter
from .views import UsersViewset, UserInfoViewset


user_router = DefaultRouter()
user_router.register(r'users', UsersViewset, base_name="users")
user_router.register(r'userInfo', UserInfoViewset, base_name="userInfo")
