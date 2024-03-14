from django.urls import path, re_path

from . import views

app_name = 'products'

urlpatterns = [
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('', views.ProductListView.as_view(), name='list'),
    re_path(r'(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name='detail'),
]
