from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import CustomUser
from .forms import CreateChatForm
from .models import Chat
# Create your views here.


@login_required
def chat(request):
    # Find existing users (ManyToMany keeps track of pks)
    chats = Chat.objects.filter(users=request.user.pk)
    return render(request, 'chat/chat.html', {'chats': chats})


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
