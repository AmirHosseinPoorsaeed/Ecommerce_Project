from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from allauth.account.views import PasswordChangeView as AllAuthPasswordChangeView

from .forms import PhoneNumberForm, VerifyForm
from .utils import generate_random_otp, verify_otp_code
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
                cache_key = f'otp_{phone_number}'
                cache.set(cache_key, otp_code, 180)
                request.session['phone_number'] = str(phone_number)
                print(otp_code)
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'User with this phone number does not exists.')
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
                    return redirect('pages:home')
                else:
                    messages.error(request, 'Authenticatin faild.')
            else:
                messages.error(request, 'Invalid OTP code.')

    else:
        form = VerifyForm()

    return render(request, 'account/verify_otp.html', {'form': form})


class CustomPasswordChangeView(AllAuthPasswordChangeView):
    success_url = reverse_lazy('pages:home')
