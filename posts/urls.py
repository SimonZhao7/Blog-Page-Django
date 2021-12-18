from django.urls import path
from . import views


app_name = 'posts'


urlpatterns = [
    path('', views.list_posts, name='list'),
    path('lazy_load_posts', views.lazy_load_posts, name='lazy_list'),
    path('create/', views.create_post, name='create'),
    path('like/', views.like, name='like'),
    path('unlike/', views.unlike, name='unlike'),
]