from django.http.response import HttpResponse, JsonResponse
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import CustomUser
from notifications.views import get_count
from .forms import CreatePostForm, ReplyForm
from .models import Post, Comment

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
def comments(request, slug):
    try:
        post = Post.objects.get(id=Post.get_id(slug))
    except:
        return render(request, '404.html')
    
    comments = post.comment_set.filter(is_reply=False)
    if request.method == 'POST':
        new_comment = Comment(user=request.user, message=request.POST.get('comment'), post=post)
        new_comment.save()
        return JsonResponse({'comment_slug': new_comment.get_slug()})
    return render(request, 'posts/comments.html', {'post': post, 'comments': comments})

@login_required
def reply_comment(request, slug):
    try:
        comment = Comment.objects.get(id=Comment.get_id(slug))
    except:
        return render(request, '404.html')
    
    form = ReplyForm()
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = comment.post
            reply.is_reply = True
            reply.save()
            comment.comment_set.add(reply)
            slug = comment.post.get_slug()
            return redirect('posts:comments', slug=slug)
    return render(request, 'posts/reply_comment.html', {'form': form})

@login_required
def delete_comment(request, slug):
    try:
        comment = Comment.objects.get(id=Comment.get_id(slug))
    except:
        return render(request, '404.html')
    
    # Delete its reply chain as well
    if not comment.is_reply:
        for reply in comment.comment_set.all():
            reply.delete()
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])

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