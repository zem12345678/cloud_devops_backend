from django.contrib import admin
from .models import Author, Publish, Book

#@admin.register(Author)
class BookAdmin(admin.ModelAdmin):

       search_fields = ('name',)                                    # 搜索框，可以按书名搜索，可以是列表或者元组

       list_display = ('name','publisher','publication_date',)      # 列出标题和时间，

       list_editable = ('publication_date',)                        # 可直接编辑的列

       ordering = ('publication_date',)                  # 并可以根据时间排序升降序可以自己调节

       raw_id_fields = ('publisher',)   			     # 将ForeignKey字段从‘下拉框’改变为‘文本框’显示

       list_per_page =10                                 # 分页，每页10条数据

       # 这行代码添加一个“Filter”侧边栏，可以使人们通过pub_date字段对变更列表进行过滤：       
       list_filter = ('publication_date','publisher',)         

       # 左边是备选列表，右边是选择列表，只适用于manytomany的表
       filter_horizontal = ('authors',)       

       # 和上面一样，只是两个选择框是上下结构.
       # filter_vertical=('authors',)    


admin.site.register(Book,BookAdmin)
admin.site.register(Author)
admin.site.register(Publish)

