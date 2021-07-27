from django import forms


class CreateChatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['users'] = forms.MultipleChoiceField(
            choices=self.setup_choices(), required=True, widget=forms.SelectMultiple(attrs={'class': 'user-select', 'multiple': 'multiple', 'style': 'width: 100%;'})
        )

    def setup_choices(self):
        USER_CHOICES = []
        for friend in self.user.userfriend_set.all():
            USER_CHOICES.append((friend.friend, friend.friend.username))
        return USER_CHOICES

    chat_name = forms.CharField(max_length=50)