from rest_framework.routers import DefaultRouter
from .views import GroupViewset, GroupMembersViewset, GroupPermissionViewset


group_router = DefaultRouter()
group_router.register(r'groups', GroupViewset, base_name="groups")
group_router.register(r'groups/members', GroupMembersViewset, base_name="members")
group_router.register(r'groups/permission', GroupPermissionViewset, base_name="permission")