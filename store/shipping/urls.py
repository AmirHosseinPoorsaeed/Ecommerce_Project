from django.urls import path

from . import views

app_name = 'shipping'

urlpatterns = [
    path('', views.shipping_create_view, name='create'),
    path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
]
