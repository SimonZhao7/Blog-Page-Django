from django.urls import path
from . import views

app_name = 'search'


urlpatterns = [
    path('', views.get_results, name='get_results'),
]