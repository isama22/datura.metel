from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('post/', views.post, name="post"),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),

    path('posts/create/', views.PostCreate.as_view(), name="posts_create"),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),

    # auth
    path('accounts/signup/', views.signup, name='signup'),

    #photo
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),

    #profile page
    # path('profile/', views.ProfileObjectMixin, name='profile'),
    # path('profile/', views.profile, name='profile'),

    # #commenting
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('posts/comment/<int:post_id>/delete/', views.CommentDelete.as_view(), name='delete_comment'),
    path('posts/comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='delete_comment'),
]