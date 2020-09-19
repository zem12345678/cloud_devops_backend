# @Time    : 2020/7/12 14:24
# @Author  : ZhangEnmin
# @FileName: basic.py
# @Software: PyCharm

from django.contrib import admin
# Register your models here.
from .models import ApiHttpMethod, ApiPermission, ApiPermissionGroup,UserProfile


class ApiHttpMethodAdmin(admin.ModelAdmin):
    # 搜索框，可以按书名搜索，可以是列表或者元组
    search_fields = ('method', )

    # 列出标题和时间
    list_display = ('method',)


class ApiPermissionAdmin(admin.ModelAdmin):

       # 搜索框，可以按书名搜索，可以是列表或者元组
       search_fields = ('name', 'uri', )

       # 列出标题和时间
       list_display = ('name', 'uri', 'show_api_http_method')

       # 可直接编辑的列
       # list_editable = ('name', 'uri',)

       # 并可以根据时间排序升降序可以自己调节
       # ordering = ('publication_date',)

       # 将ForeignKey字段从‘下拉框’改变为‘文本框’显示
       # raw_id_fields = ('publisher',)

       list_per_page =15                                 # 分页，每页10条数据

       # 这行代码添加一个“Filter”侧边栏，可以使人们通过pub_date字段对变更列表进行过滤：
       # list_filter = ('publication_date','publisher',)

       # 左边是备选列表，右边是选择列表，只适用于manytomany的表
       filter_horizontal = ('api_http_methods',)

       # 和上面一样，只是两个选择框是上下结构.
       # filter_vertical=('authors',)

       '''展示api http method'''
       def show_api_http_method(self, obj):
           return ' | '.join([ http_method.method for http_method in obj.api_http_methods.all() ])


       show_api_http_method.short_description = 'HTTP METHOD'  # 设置表头


class ApiPermissionGroupAdmin(admin.ModelAdmin):
    # 搜索框，可以按书名搜索，可以是列表或者元组
    search_fields = ('name',)

    # 列出标题和时间
    list_display = ('name', 'show_api_permissions')

    # 可直接编辑的列
    # list_editable = ('name', )

    # 并可以根据时间排序升降序可以自己调节
    # ordering = ('publication_date',)

    # 将ForeignKey字段从‘下拉框’改变为‘文本框’显示
    # raw_id_fields = ('publisher',)

    list_per_page = 15  # 分页，每页10条数据

    # 这行代码添加一个“Filter”侧边栏，可以使人们通过pub_date字段对变更列表进行过滤：
    # list_filter = ('publication_date','publisher',)

    # 左边是备选列表，右边是选择列表，只适用于manytomany的表
    filter_horizontal = ('api_permissions', "users")

    # 和上面一样，只是两个选择框是上下结构.
    # filter_vertical=('authors',)

    '''展示api http method'''

    def show_api_permissions(self, obj):
        retdata = []
        for perm in obj.api_permissions.all():
            lineMsg = "{}: {}".format(perm.name, perm.uri)
            retdata.append(lineMsg)
        return " | ".join(retdata)

    show_api_permissions.short_description = 'API权限详情'  # 设置表头


class UserProfileAdmin(admin.ModelAdmin):

    search_fields = ('username', )
    list_display=('username', 'name', 'mobile', 'password')
    # exclude = ('birth_date',)

    # 是否在列表下方显示actions的下拉框，默认为False。
    actions_on_bottom = True

    # 根据你指定的日期相关的字段，为页面创建一个时间导航栏，可通过日期过滤对象。例如：
    date_hierarchy = 'date_joined'

    empty_value_display = '-empty-'


# 参考文章
# https://blog.csdn.net/weixin_34023982/article/details/92535539
# https://www.cnblogs.com/wumingxiaoyao/p/6928297.html

# 页面标题
admin.site.site_title = "自动化运维云平台 | 超管平台"

# 登录页导航条和首页导航条标题
admin.site.site_header = "自动化运维云平台"

# 主页标题
admin.site.index_title = "欢迎登陆"

admin.site.register(UserProfile, UserProfileAdmin)

# 注册绑定
admin.site.register(ApiPermission, ApiPermissionAdmin)
admin.site.register(ApiHttpMethod, ApiHttpMethodAdmin)
admin.site.register(ApiPermissionGroup, ApiPermissionGroupAdmin)
