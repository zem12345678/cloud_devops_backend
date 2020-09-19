from django.contrib.auth.models import Permission,Group
from .models import UserProfile,PmsPermission
def get_permission_obj(pid):
    try:
        return Permission.objects.get(pk=pid)
    except Permission.DoesNotExist:
        return None

def get_user_obj(uid):
    try:
        for user_id in uid:
            if UserProfile.objects.get(pk=user_id):
                pass
        return uid
    except UserProfile.DoesNotExist:
        return None

def get_group_obj(gid):
    try:
        return Group.objects.get(pk=gid)
    except Group.DoesNotExist:
        return None

def get_permission_pid(pid):
    try:
        for permission_id in pid:
            if Permission.objects.get(pk=permission_id):
                pass
        return pid
    except UserProfile.DoesNotExist:
        return None