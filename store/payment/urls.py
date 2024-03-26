from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process_sandbox_view, name='process'),
    path('callback/', views.payment_callback_sandbox_view, name='callback'),
]
