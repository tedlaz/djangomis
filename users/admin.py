from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from . import forms

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    model = CustomUser
    # list_display = ['email', 'username', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
