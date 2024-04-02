from django.urls import path, re_path

from . import views

app_name = 'products'

urlpatterns = [
    path('favorite/add/<int:product_id>/', views.product_favorite, name='add_favorite'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('wishlist/', views.WishListView.as_view(), name='wish_list'),
    path('', views.ProductListView.as_view(), name='list'),
    re_path(r'(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name='detail'),
]
