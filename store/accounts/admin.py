from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import date2jalali

from .models import CustomUser, Customer
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


@admin.register(Customer)
class CustomerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'get_birth_date_jalali', 'age',)
    search_fields = ('username', 'last_name', 'first_name',)

    @admin.display(description='Birth Date')
    def get_birth_date_jalali(self, customer):
        if customer.birth_date:
            return date2jalali(customer.birth_date).strftime('%d %b %Y')
        return
