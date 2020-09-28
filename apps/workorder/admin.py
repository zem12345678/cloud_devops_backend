from django.contrib import admin
from .models import WorkOrder
# Register your models here.
class WorkOrderAdmin(admin.ModelAdmin):
    # 搜索框，可以按书名搜索，可以是列表或者元组
    search_fields = ('title','applicant')

    # 列出标题和时间
    list_display = (
        'title',
        'order_contents',
        'status',
        'apply_time'
    )

    # 将ForeignKey字段从‘下拉框’改变为‘文本框’显示
    raw_id_fields = (
        'applicant',
        'assign_to',
        'final_processor'
    )

    list_per_page = 15


# 注册绑定
admin.site.register(WorkOrder, WorkOrderAdmin)