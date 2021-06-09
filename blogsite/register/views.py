from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .models import RegisterForm

# Create your views here.


def register(response):
    form = RegisterForm()
    if response.POST.get('submit') == 'sign up':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
    return render(response, "register/login.html", {'form': form})
