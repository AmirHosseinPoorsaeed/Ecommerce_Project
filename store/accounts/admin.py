from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


UserAdmin.fieldsets[1][1]['fields'] = (
    ('first_name', 'last_name', 'email', 'phone_number')
)

UserAdmin.add_fieldsets[0][1]['fields'] = (
    ('username', 'phone_number', 'email', 'password1', 'password2')
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
