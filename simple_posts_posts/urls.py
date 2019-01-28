from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('create_comment/<int:post_id>/', views.create_comment, name='create_comment'),
    path('comment_list/<int:post_id>/', views.comment_list, name='comment_list'),
    path('post_detail/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:id>/', views.post_detail, name='post_detail'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('unlike_post/<int:post_id>/', views.unlike_post, name='unlike_post'),
    path('most_liked/', views.most_liked, name='most_liked'),
]