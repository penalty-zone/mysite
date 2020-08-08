import datetime


from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum

from .models import ReadNum,ReadDetail
from blog.models import Blog


#基础计数
def read_statistics_once_read(request,obj):
    #使用了ContentType这个得到的是ContentType这个类型的值
    #这个值并不代表是直接的  obj字符串对应的模型 ，而是一个ContentType类型的Blog ######
    content_1 = ContentType.objects.get_for_model(obj)
    key = "{}_{}_read".format(content_1.model, obj.pk)
    if not request.COOKIES.get(key):
 #基础的使用if else判断的方法
            # if ReadNum.objects.filter(content_type=content_1, object_id=obj.pk).count():
            #     readnum = ReadNum.objects.get(content_type=content_1, object_id=obj.pk)
            # else:
            #     readnum = ReadNum(content_type=content_1, object_id=obj.pk)
                # 如果不添加这个的话则会一直判别为错   因为;如果不在ReadNum中创建一条对应的blog则对应的Blog.blog中不会存在 readnum
                # 也可以这样写，也是和上面的一样
                # readnum.content_type = content_1
                # readnum.object_id = blog.pk
 #使用get_or_create方法
 #阅读计数加1
            readnum, create = ReadNum.objects.get_or_create(content_type=content_1, object_id=obj.pk)
            readnum.read_num += 1
            readnum.save()

 #基础的使用if else判断的方法
            # if ReadDetail.objects.filter(content_type=content_1, object_id=obj.pk, date=date).count():
            #     readdetail = ReadDetail.objects.get(content_type=content_1, object_id=obj.pk, date=date)
            # else:
            #     readdetail = ReadDetail(content_type=content_1, object_id=obj.pk, date=date)
 # 使用get_or_create, 
 #当天阅读数+1
            date = timezone.now().date()
            readdetail, create = ReadDetail.objects.get_or_create(content_type=content_1, object_id=obj.pk, date=date)
            readdetail.read_num += 1
            readdetail.save()
    return key

#取出阅读数
def get_seven_days_read_data(content_type):
    today = timezone.now().date() #包含日期和时间
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)

    return dates, read_nums

#今日热点数据
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]

#昨日热点数据
def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects \
        .filter(content_type=content_type, date=yesterday) \
        .order_by('-read_num')
    return read_details[:7]

# 一周热点数据用这个方法  content_type==这里传递的和别的传递的不同需要传递原blog
def get_seven_days_hot_blogs(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = content_type.objects.filter(read_details__date__lt=today,read_details__date__gte=date) \
        .values('id','title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


#一周热点数据这个方法不好，实用的在view中写了
    # def get_7_days_hot_data(content_type):
    #     today = timezone.now().date()
    #     date = today - datetime.timedelta(days=7)
    #     read_details = ReadDetail.objects \
    #         .filter(content_type=content_type, date__lt=today,date__gte=date) \
    #         .values('content_type', 'object_id') \
    #         .annotate(read_num_sum=Sum('read_num')) \
    #         .order_by('-read_num_sum')
    #     return read_details[:7]




