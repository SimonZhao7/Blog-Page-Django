from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('change-username/', views.change_username, name='change_username'),
    path('change-password/', views.change_password, name="change_password"),
    path('<username>/', views.profile, name='profile'),
]