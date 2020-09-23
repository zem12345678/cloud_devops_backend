from django.contrib.auth.models import Permission,Group
from .models import UserProfile,PmsPermission,Menu
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

def get_menu_object(pk):
    try:
        return Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return None


def get_menu_tree(queryset, group_queryset=None):
    ret = []
    first_menus = _get_first_menu(queryset)
    for obj in first_menus:
        node = _get_menu_node(obj, group_queryset)
        node["children"] = _get_menu_children(queryset.filter(pid__exact=obj), group_queryset)
        ret.append(node)
    return ret


def _get_first_menu(queryset):
    ret = []
    def check_exists(obj):
        if obj in ret:
            return True
        return False
    for obj in queryset:
        if obj.pid:
            # 当前菜单为二级
            if not check_exists(obj.pid):
                ret.append(obj.pid)
        else:
            if not check_exists(obj):
                ret.append(obj)
    return ret


def _get_menu_children(queryset, group_queryset=None):
    ret = []
    for obj in queryset:
        ret.append(_get_menu_node(obj, group_queryset))
    return ret


def _get_menu_node(menu_obj, group_queryset=None):
    node = {}
    node["id"] = menu_obj.id
    node["path"] = menu_obj.path
    node["label"] = menu_obj.title
    node['icon'] = menu_obj.icon if menu_obj.icon else ""
    node['show'] = menu_obj.show
    node["pid"] = _get_menu_parent(menu_obj)
    if group_queryset is not None:
        node["permission"] = _get_menu_permission(menu_obj, group_queryset)
    return node


def _get_menu_parent(menu_obj):
    try:
        return menu_obj.pid.id
    except:
        return 0


def _get_menu_permission(menu_obj, group_queryset=None):
    if group_queryset is None:
        return True
    try:
        group_queryset.get(pk=menu_obj.id)
        return True
    except:
        return False