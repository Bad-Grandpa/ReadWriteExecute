from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import LJUser


class LJUserCreationForm(UserCreationForm):
    class Meta:
        model = LJUser
        fields = UserCreationForm.Meta.fields


class LJUserChangeForm(UserChangeForm):
    class Meta:
        model = LJUser
        fields = UserChangeForm.Meta.fields