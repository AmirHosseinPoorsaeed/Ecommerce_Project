"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = 'Store Management'
admin.site.index_title = 'Website Management'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('accounts/', include('store.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('', include('store.pages.urls', namespace='pages')),
    path('products/', include('store.products.urls', namespace='products')),
    path('comments/', include('store.comments.urls', namespace='comments')),
    path('qas/', include('store.qas.urls', namespace='qas')),
    path('cart/', include('store.cart.urls', namespace='cart')),
    path('search/', include('store.search.urls', namespace='search')),
    path('shipping/', include('store.shipping.urls', namespace='shipping')),
    path('orders/', include('store.orders.urls', namespace='orders')),
    path('coupons/', include('store.coupons.urls', namespace='coupons')),
    path('payment/', include('store.payment.urls', namespace='payment')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
