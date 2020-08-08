from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .models import BlogType, Blog
from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 分页器
    page_num = request.GET.get('page', 1)#  默认打开为第4页 且 获取到传入的GET请求
    page_of_blogs = paginator.get_page(page_num)  #  将当前信息保存传入到页面中
    current_page_num = page_of_blogs.number # 当前那一页
    # if current_page_num == 1:
    #     page_range = [current_page_num, current_page_num+1, current_page_num+2]
    # elif current_page_num == 2:
    #     page_range = [current_page_num-1, current_page_num, current_page_num+1, current_page_num+2]
    # elif current_page_num == paginator.num_pages:
    #     page_range = [current_page_num-2, current_page_num-1,
    #     current_page_num]
    # elif current_page_num == paginator.num_pages-1:
    #     page_range = [current_page_num-2, current_page_num-1,
    #     current_page_num, current_page_num+1]
    # else:
    #     page_range = [current_page_num-2, current_page_num-1,
    #     current_page_num, current_page_num+1, current_page_num+2]
    page_range = list(range(max(current_page_num - 2, 1), current_page_num))+\
     list(range(current_page_num, min(current_page_num+2, paginator.num_pages)+1))
    #加上省略标记
    if page_range[0] -1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')


    # 加上首页和尾页 
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}

    # 获取博客的类型总数和
    blog_types = BlogType.objects.all()
    blog_types_list = []                # 下面的blog_type，就是用类对应出来的
    for blog_type in blog_types:  #   下面传递的是blog_type完全理解不了为什么传入的是对象，而对象却能用来检索
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    # 获取日期的数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates: #  这里的blog_conunt 数据变量
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count



    # 由于传递了 page_of_list 而 .object_list 是其中的方法所以没必要传入上面的值
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list#  这里的month  是所有blog拿到年和月
    context['blog_dates'] = blog_dates_dict
    context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = blog_types_list
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()

    context = get_blog_list_common_data(request,blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk) # 拿到当前博客的类型
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    # 由于传递了 page_of_list 而 .object_list 是其中的方法所以没必要传入上面的值
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    # blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)

    context = get_blog_list_common_data(request,blogs_all_list)
    # 由于传递了 page_of_list 而 .object_list 是其中的方法所以没必要传入上面的值
    context['blogs_with_date'] = '{}年{}月'.format(year, month)
    return render(request, 'blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk = blog_pk) # 拿到当前的博客   
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['blog'] = blog

    #下面的东西使用了comment_tags,自定义模板标签代替了
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)
    # context['comments'] = comments.order_by('-comment_time')
    # data={}
    # data['content_type'] = blog_content_type.model #模型对应的字符串
    # data['object_id'] = blog_pk
    # data['reply_comment_id'] = 0
    # context['comment_form'] = CommentForm(initial=data)

    response = render(request,'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true', max_age=None,expires=None) #阅读cookie标记
    return response

























# url中
# path('detail/<blog_id>', views.detail, name="详情")
# view中
# context【'blog'】 = get_object_or_404(Blog, id=blog_id)
# detail.html网页中
# <a href="{% url 'diary:详情' blog.id %}">

