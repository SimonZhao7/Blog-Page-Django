from django.urls import path
from . import views


app_name = 'notifications'


urlpatterns = [
    path('', views.list_notifications, name="list"),
    path('delete', views.delete_notifications, name="delete"),
]