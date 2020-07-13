from django.contrib import admin
from django.contrib.auth.models import User, Group


# Register your models here.
from .models import UserProfile



class UserProfileAdmin(admin.ModelAdmin):

    search_fields = ('username', )
    list_display=('username', 'name', 'phone', 'password')
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
admin.site.site_title = "51Reboot | 高级课程"

# 登录页导航条和首页导航条标题
admin.site.site_header = "51Reboot 运维平台"

# 主页标题
admin.site.index_title = "欢迎登陆"

admin.site.register(UserProfile, UserProfileAdmin)
