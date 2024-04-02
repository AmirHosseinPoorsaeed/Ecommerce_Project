from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm as AllAuthSignupForm
from phonenumber_field.formfields import PhoneNumberField
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from store.accounts.models import Customer

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username',)


class CustomSignupForm(AllAuthSignupForm):
    phone_number = PhoneNumberField(region='IR', label=_('Your Phone Number'))

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if not User.objects.filter(phone_number=data).exists():
            return data
        raise forms.ValidationError('User with this phone number already exists.')

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user


class PhoneNumberForm(forms.Form):
    phone_number = PhoneNumberField(region='IR', label=_('Your Phone Number'))


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=5)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('birth_date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'] = JalaliDateField(
            label='date',
            widget=AdminJalaliDateWidget()
        )
