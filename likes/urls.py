from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/comment/update_comment
    path('like_change', views.like_change, name='like_change')
    
]