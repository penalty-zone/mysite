from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/comment/update_comment
    path('login/', views.login, name='login'),
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register_2/', views.register_2, name='sign_for_medal'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('change_email/', views.change_email, name='change_email'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]