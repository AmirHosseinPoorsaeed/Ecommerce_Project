from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from allauth.account.views import PasswordChangeView as AllAuthPasswordChangeView

from .forms import PhoneNumberForm, VerifyForm, ProfileUpdateForm, UserUpdateForm
from .utils import generate_random_otp, verify_otp_code, store_otp_in_cache
from .decorators import unauthenticated_required

User = get_user_model()


@unauthenticated_required
def send_otp(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if User.objects.filter(phone_number=phone_number).exists():
                otp_code = generate_random_otp()
                store_otp_in_cache(phone_number, otp_code)
                request.session['phone_number'] = str(phone_number)
                print(otp_code)
                messages.success(request, _('Code sent successfully'))
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, _('User with this phone number does not exists.'))
    else:
        form = PhoneNumberForm()

    return render(request, 'account/login_otp.html', {'form': form})


def verify_otp(request):
    phone_number = request.session.get('phone_number')

    if not phone_number:
        return redirect('accounts:send_otp')

    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if verify_otp_code(code, phone_number):
                user = authenticate(request, username=phone_number)
                if user is not None:
                    login(request, user)
                    del request.session['phone_number']
                    messages.success(request, _('Authentication successfully.'))
                    return redirect('pages:home')
                else:
                    messages.error(request, _('Authentication faild.'))
            else:
                messages.error(request, _('Invalid OTP code.'))

    else:
        form = VerifyForm()

    return render(request, 'account/verify_otp.html', {'form': form})


class CustomPasswordChangeView(AllAuthPasswordChangeView):
    success_url = reverse_lazy('pages:home')


@login_required
def profile(request):

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            instance=request.user.customer
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your account has been updated.'))
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.customer)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
