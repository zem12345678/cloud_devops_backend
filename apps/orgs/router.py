from rest_framework.routers import DefaultRouter
from .views import GroupViewset, GroupMembersViewset, GroupPermissionViewset


org_router = DefaultRouter()
org_router.register(r'orgs', GroupViewset, base_name="groups")
org_router.register(r'orgs/members', GroupMembersViewset, base_name="members")
org_router.register(r'orgs/permission', GroupPermissionViewset, base_name="permission")