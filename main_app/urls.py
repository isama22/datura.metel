from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('post/', views.post, name="post"),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
]