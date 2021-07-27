from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import CustomUser
from .forms import CreateChatForm
from .models import Chat
# Create your views here.


@login_required
def chat(request):
    return render(request, 'chat/chat.html', {})


@login_required
def create(request):
    form = CreateChatForm(user=request.user)

    if request.method == 'POST':
        form = CreateChatForm(request.POST, user=request.user)
        # check if chat exists
        if form.is_valid():
            new_chat = Chat(name=form.cleaned_data['chat_name'])
            new_chat.save()
            for user in form.cleaned_data['users']:
                user = CustomUser.objects.get(username=user)
                new_chat.users.add(user)
            return redirect('/chat')
    return render(request, 'chat/create.html', {'form': form})
