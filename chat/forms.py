from django import forms
from .models import Chat, Messages
from account.models import CustomUser
from django.core.exceptions import ValidationError


class CreateChatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['users'] = forms.MultipleChoiceField(
            choices=self.setup_choices(), required=True, widget=forms.SelectMultiple(attrs={'class': 'user-select', 'multiple': 'multiple', 'style': 'width: 100%;'})
        )

    chat_name = forms.CharField(max_length=50)

    def clean(self):
        data = self.cleaned_data
        users = data['users']
        users.append(self.user.username)  # Add yourself as a chat member

        # Check if chat already exists
        for chat in Chat.objects.all():
            if set(users) == self.change_to_list(chat):
                raise ValidationError('You have already created a chat with these users.')
        return data

    def setup_choices(self):
        USER_CHOICES = []
        for friend in self.user.userfriend_set.all():
            USER_CHOICES.append((friend.friend, friend.friend.username))
        return USER_CHOICES

    def change_to_list(self, chat_obj):
        user_list = []
        for user in chat_obj.users.all():
            user_list.append(user.username)
        return set(user_list)

    def save(self):
        new_chat = Chat(name=self.cleaned_data['chat_name'])
        new_chat.save()
        for other_user in self.cleaned_data['users']:
            other_user_obj = CustomUser.objects.get(username=other_user)
            new_chat.users.add(other_user_obj)
        new_chat.save()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 1, 'class': 'form-field', 'style': 'resize: none; flex: 13;'})
        }
