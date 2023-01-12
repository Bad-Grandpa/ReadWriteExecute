from django.forms import TextInput, PasswordInput, CharField
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm,
    UsernameField
)

from .models import LJUser


class LJUserCreationForm(UserCreationForm):
    class Meta:
        model = LJUser
        fields = UserCreationForm.Meta.fields


class LJUserChangeForm(UserChangeForm):
    class Meta:
        model = LJUser
        fields = UserChangeForm.Meta.fields


class LJUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LJUserLoginForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    username = UsernameField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'id': 'floatingInput',
            }
        )
    )
    password = CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'id': 'floatingPassword',
            }
        )
    )