from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# User = get_user_model()
from users.models import User


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")
