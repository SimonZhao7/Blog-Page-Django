from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import CustomUser
from notifications.views import get_count
from .forms import CreatePostForm
from .models import Post

# Create your views here.


@login_required
def list_posts(request):
    all_posts = Post.objects.all().order_by('date_time_posted').reverse()
    return render(request, 'posts/list.html', {'posts': all_posts, 'notif_count': get_count(request)})

@login_required
def create_post(request):
    form = CreatePostForm(user=request.user)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully created a post.')
    return render(request, 'posts/create.html', {'form': form, 'notif_count': get_count(request)})

@login_required
def like(request):
    if request.method == 'POST':
        post = Post.objects.get(id=Post.get_id(request.POST.get('slug')))
        user = CustomUser.objects.get(username=request.POST.get('liker'))
        post.users_liked.add(user)
        post.likes += 1
        post.save()
        return HttpResponse()
    return redirect('posts:list')

@login_required
def unlike(request):
    if request.method == 'POST':
        post = Post.objects.get(id=Post.get_id(request.POST.get('slug')))
        user = CustomUser.objects.get(username=request.POST.get('liker'))
        post.users_liked.remove(user)
        post.likes -= 1
        post.save()
        return HttpResponse()
    return redirect('posts:list')