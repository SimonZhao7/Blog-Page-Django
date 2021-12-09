from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import CustomUser
from .forms import CreateChatForm, MessageForm
from .models import Chat
# Create your views here.


@login_required
def inbox(request):
    # Find existing users (ManyToMany keeps track of pks)
    chats = Chat.objects.filter(users=request.user.pk)
    return render(request, 'chat/inbox.html', {'chats': chats})


@login_required
def create(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    form = CreateChatForm(user=user)

    if request.method == 'POST':
        form = CreateChatForm(request.POST, user=user)
        # check if chat exists
        if form.is_valid():
            form.save()
            return redirect('/chat')
    return render(request, 'chat/create.html', {'form': form})


@login_required
def chat(request, slug):
    chats = Chat.objects.filter(users=request.user.pk)
    try:
        desired_chat = Chat.objects.get(pk=Chat.get_id(slug), users=request.user.pk)
    except Chat.DoesNotExist:  # No id or not a user of chat
        return redirect('chat:inbox')
    return render(request, 'chat/chat.html', {'chats': chats, 'chat': desired_chat})
