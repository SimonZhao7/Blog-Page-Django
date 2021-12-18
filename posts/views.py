from django.http.response import HttpResponse, JsonResponse
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.template import loader
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
    return render(request, 'posts/list.html', {'posts': all_posts[:10], 'notif_count': get_count(request)})


def lazy_load_posts(request):
    page = request.POST.get('page')
    posts = Post.objects.all().order_by('date_time_posted').reverse()
    
    results_per_page = 10
    paginator = Paginator(posts, results_per_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(2)
        page = 2
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Renders the html to add to list.html
    posts_html = loader.render_to_string('posts/post_content.html', {'posts': posts})
    
    # Returns JSON for success function
    output_data = {'posts_html': posts_html, 'has_next': posts.has_next(), 'page': page}
    return JsonResponse(output_data)
    

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