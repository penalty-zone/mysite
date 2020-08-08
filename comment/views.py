from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse

from .models import Comment
from .forms import CommentForm
from django.utils import timezone


#高级一点的判断和评论，判断封装在forms中,  在调用is_valid时会自动调用clean
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        #检查保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()

        #发送邮件
        comment.send_email()

        #返回JSON数据
        data = {}
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        # data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_time'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        data['content_Type'] = ContentType.objects.get_for_model(comment).model  # .model这是获取ContentType类型对应模型所对应的字符串                                                                         # .model_class() 这是获取ContentType类型对应的那个模型
        if not parent is None:
            #  comment.reply_to不是一个可以序列化的USER 要用他的str才行
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
        return JsonResponse(data)
        # return redirect(referer)  #之前用的不是异步请求
    else:
        data = {}
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
        return JsonResponse(data)
        #之前用的不是异步请求
        # return render(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})
        



#初始的判断以及评论
    '''referer = request.META.get('HTTP_REFERER', reverse('home'))
    user = request.user
    #数据检查
    if not user.is_authenticated:
        return render(request,'error.html',{'message':'用户名未登录','redirect_to':referer})



    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request,'error.html',{'message':'评论内容为空','redirect_to':referer})



    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        #使用了ContentType这个得到的是ContentType这个类型的值
        #我们要得到专门的Blog所以要使用      .model_class
        model_class = ContentType.objects.get(model=content_type).model_class()

        #这里的model_class才是真的 Blog这个模型  ，而ContentType只是用来检索的模型
        #model_class---->Blog    ContentType.objects.get(model=content_type)---->ContentType(Blog)
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request,'error.html',{'message':'评论对象不存在','redirect_to':referer})

    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    #在views中修改或者利用动态创建的方法给模型赋值则需要保存
    comment.save()
    return redirect(referer)'''





