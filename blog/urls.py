from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='blog-home'),
    path('posts/<str:slug>', views.post_detail, name='post-detail'),
    path('likes/<str:slug>', views.like_view, name='like_post'),
    path('add', views.add_post, name='post-create'),
    path('posts/<str:slug>/update', views.update_post, name='update-post'),
    path('posts/<str:slug>/delete', views.delete_post, name='delete-post'),
    path('comments/<str:slug>/delete', views.delete_comment, name='delete-comment'),
    path('about', views.about, name='about'),

]