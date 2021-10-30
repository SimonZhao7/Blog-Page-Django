from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('create/', views.create, name='create'),
    path('message/<slug:slug>/', views.chat, name='chat'),
]