from django.contrib import admin
from .models import BlogType, Blog
# Register your models here.
@admin.register(BlogType)
class  BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
@admin.register(Blog)
class  BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_read_num', 'blog_type', 'author','created_time', 'last_updated_time')
 





# 最早比较单一的计数方法
    '''
    #   如果外键绑定到        
    @admin.register(ReadNum)
    class  ReadNumAdmin(admin.ModelAdmin):
        list_display = ('read_num', 'blog')
    '''









