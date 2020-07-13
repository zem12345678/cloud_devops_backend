from django.contrib import admin

# Register your models here.
from .models import BasicTicketTemplate 
from .models import TicketDetail 




class BasicTicketTemplateAdmin(admin.ModelAdmin):

       # 搜索框，可以按书名搜索，可以是列表或者元组
       search_fields = ('name', 'type', 'status')

       # 列出标题和时间
       list_display = (
           'f_title',
           't_title',
           'content',
       )

       # 将ForeignKey字段从‘下拉框’改变为‘文本框’显示
       raw_id_fields = (
           'examine',
           'executor',
       )

       list_per_page = 15



class TicketDetailAdmin(admin.ModelAdmin):

       # 搜索框，可以按书名搜索，可以是列表或者元组
       search_fields = ('name', )

       # 列出标题和时间
       list_display = (
           'name',
           'content',
           'status',
       )

       # 将ForeignKey字段从‘下拉框’改变为‘文本框’显示
       raw_id_fields = (
           'creator',
           'template',
       )

       list_per_page = 15

# 注册绑定
admin.site.register(BasicTicketTemplate, BasicTicketTemplateAdmin)
admin.site.register(TicketDetail, TicketDetailAdmin)
