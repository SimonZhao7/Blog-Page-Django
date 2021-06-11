from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from .forms import RegisterForm

# Create your views here.


def login(request):
    form = AuthenticationForm()
    if request.POST.get('submit') == 'log in':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = Profile.objects.get(username=form.cleaned_data["username"])
            user_login(request, user)
            return redirect('/account/profile/')
    return render(request, "register/login.html", {"form": form})


def register(request):
    form = RegisterForm()
    if request.POST.get('submit') == 'sign up':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "register/register.html", {'form': form})
