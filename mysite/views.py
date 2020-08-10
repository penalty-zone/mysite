from django.core.cache import cache
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_seven_days_hot_blogs
from blog.models import Blog

#使用反向链接来进行查询七天的热门
    # def get_seven_days_hot_blogs():
    #     today = timezone.now().date()
    #     date = today - datetime.timedelta(days=7)
    #     blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date) \
    #         .values('id','title') \
    #         .annotate(read_num_sum=Sum('read_details__read_num')) \
    #         .order_by('-read_num_sum')
    #     return blogs[:7]
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)


    #获取7天热门缓存数据
    seven_hot_data = cache.get('seven_hot_data')
    if seven_hot_data is None:
        seven_hot_data = get_seven_days_hot_blogs(Blog)
        cache.set('seven_hot_data', seven_hot_data, 3600)
    # seven_hot_data = get_seven_days_hot_blogs(Blog)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    # seven_hot_data = get_7_days_hot_data(blog_content_type)  这个不完美，原博客中的取不出来因为（values）
    
    #这里利用了缓存机制在上面
    # seven_hot_data = get_seven_days_hot_blogs(Blog) #这里传递的是Blog ####
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates 
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['seven_hot_data'] = seven_hot_data
    return render(request, 'home.html', context)





