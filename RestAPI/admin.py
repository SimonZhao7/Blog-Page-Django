from account.models import CustomUser
from rest_framework.authtoken.models import Token

for user in CustomUser.objects.all():
    Token.objects.get_or_create(user=user)