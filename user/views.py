import datetime
import string
import random
import time
from django.utils import timezone
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import auth
from django.urls import reverse #反向解析，使该页面可以使用 URLS中页面的别名
from django.contrib.auth.models import User
from .forms import LoginForm,RegForm,ChangeNicknameForm, BindEmailForm,ChangePassword,ForgotPasswordForm
from django.http import JsonResponse
from .models import Profile
from django.core.mail import send_mail

#在评论区登录
def login(request):
    context = {}
    if request.method  == 'POST':
        login_form = LoginForm(request.POST)
        #is_valid验证其中的数据
        if login_form.is_valid():
            # cleaned_data  清理数据
            user = login_form.cleaned_data['user']    
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context['login_form'] = login_form
    return render(request,'user/login.html', context)

#在评论区注册
def register(request):
    context = {}

    if request.method  == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户1
            user =  User.objects.create_user(username,email,password)
            user.save()
            #清楚session
            del request.session['register_code']

            #用户登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context['reg_form'] = reg_form
    return render(request,'user/register.html', context)


#在导航栏中注册
def register_2(request):
    data = {}
    reg_form = RegForm(request.POST, request=request)
    if reg_form.is_valid():
        username = reg_form.cleaned_data['username']
        email = reg_form.cleaned_data['email']
        password = reg_form.cleaned_data['password_again']
        #创建用户1
        user =  User.objects.create_user(username,email,password)
        user.save()
        #清楚session
        del request.session['register_code']
        #用户登录

        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        data['status']='SUCCESS'
    else:
        data['status']="ERROR"
        data['reg_form_error'] = reg_form.errors.as_text()
    return JsonResponse(data)



def login_for_medal(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        # cleaned_data  清理数据
        user = login_form.cleaned_data['user']    
        auth.login(request, user)
        data={}
        data['status'] = 'SUCCESS'
    else:
        data={}
        data['status'] = 'ERROR' 
    return JsonResponse(data)

def logout(request):
    auth.logout(request)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    return redirect(referer)


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

# def Change_nickname(request):
#     if request.method=='POST':
#         pass
#     else:
#         form = ChangeNicknameForm()
#     context = {}
#     context['form'] = form
#     return render(request, '', context)
def change_nickname(request):
    nickname_new = request.POST.get('nickname', '').strip()
    user = request.user
    if len(nickname_new) < 20 and len(nickname_new)>1:
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.nickname = nickname_new
        profile.save()
        data={}
        data['status'] = 'SUCCESS'
    else:
        data={}
        data['status'] = 'ERROR'
    return JsonResponse(data)

#这个出错了
def change_email(request):
    email_new = request.POST.get('email', '')
    user = request.user
    # if len(nickname_new) < 20 and len(nickname_new)>1:
    #     profile, created = Profile.objects.get_or_create(user=request.user)
    #     profile.nickname = nickname_new
    #     profile.save()
    #     data={}
    #     data['status'] = 'SUCCESS'
    # else:
    data={}
    data['status'] = 'ERROR'
    return JsonResponse(data)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            #清楚session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}

    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get("email", "")
    send_for =request.GET.get('send_for', '')
    data = {}

    if User.objects.filter(email=email).exists():
        data['status'] = "ERROR"
        return JsonResponse(data)
    
    if email != "":
        #生产验证码
        code = "".join(random.sample(string.ascii_letters + string.digits, 4))
        
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time <30:
            data['status'] = "ERROR"
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            #发送邮件
            send_mail(
                '绑定邮箱',
                '验证码:{}'.format(code),
                '1531947807@qq.com',
                [email],
                fail_silently = False,
                )
            data['status'] = "SUCCESS"
    else:
        data['status'] = "ERROR"

    return JsonResponse(data)



def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method  == 'POST':
        form = ChangePassword(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePassword()
    context = {}

    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def forgot_password(request):

    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password =form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            #清楚session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()
    context = {}

    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)
