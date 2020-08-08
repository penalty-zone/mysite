from django.db import models
from read_statistics.models import text,ReadDetail
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name # 这里相当于是，type这个地方显示的是这个



# 这里传入的text是在计数App中的类，导入进来调用其中的方法就可以实现计数了
# 用到了，封装，迁移，继承的技术，把原本再这个类中的方法，先提出来，然后有封装到其他app中
class Blog(models.Model, text):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    read_details = GenericRelation(ReadDetail)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)




#  当创建一篇blog时，blog中相应的会存储这些字段--title--author--created_time等
    #  并且还会存储 其他外键链接到该blog上类名的小写【例如：  ReadNum-----则blog中会保存字段---readnum，readnum中包含了read_num,blog(ReadNum中的字段)】
    # b.第一种使admin中blog显示被外键链接中的某一条字段
    '''
    def get_read_num(self):  # self代表的就是当前创建的博客（某一条）
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:  # 不存在的意思
            return 0
    '''
# 
    def get_email(self):
        return self.author.email
    
    def get_url(self):
        return reverse('blog_detail',kwargs={'blog_pk':self.pk})
    
    def __str__(self):
        return "<Blog: %s>" % self.title
    
    class Meta:
        ordering = ['-created_time']
















'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    #  者里blog里面存的就是Blog使用def __str__ (): 返回回来的值
    blog = models.OneToOneField(Blog,on_delete=models.CASCADE)
'''
# a.第一种使admin中blog显示被外键链接中的某一条字段，验证了，这里的返回值就是 返回给admin中显示的且返回给了某一条blog
#          相当于让readnum == str(self.read_num)                 存在的readnum字段中
    # def __str__(self):
    #     return str(self.read_num)
