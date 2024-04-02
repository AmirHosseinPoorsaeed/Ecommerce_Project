from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('profile/', views.profile, name='profile'),
]
