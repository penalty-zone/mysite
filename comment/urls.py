from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/comment/update_comment
    path('update_comment', views.update_comment, name='update_comment')
    
]