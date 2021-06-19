from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from .forms import RegisterForm
# Create your views here.


@login_required
def profile(request, username):
    return render(request, 'account/profile.html', {"viewed_user": username})


@login_required()
def view(request):
    return render(request, 'account/profile.html', {})


def login(request):
    form = AuthenticationForm()
    if request.POST.get('submit') == 'log in':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=form.cleaned_data["username"])
            user_login(request, user)
            return redirect('/profile/')
    return render(request, "account/login.html", {"form": form})


def register(request):
    form = RegisterForm()
    if request.POST.get('submit') == 'sign up':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, "account/register.html", {'form': form})