from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import LJUserCreationForm, LJUserChangeForm
from .models import LJUser


class LJUserAdmin(UserAdmin):
    add_form = LJUserCreationForm
    form = LJUserChangeForm
    model = LJUser

    list_display = [
        'email',
        'username',
        'is_staff',
    ]


admin.site.register(LJUser, LJUserAdmin)
