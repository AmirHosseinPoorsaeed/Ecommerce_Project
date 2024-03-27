from django.contrib import admin

from .models import Stock, Sale


class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'num_sold', 'sold_at')

admin.site.register(Stock)
admin.site.register(Sale, SaleAdmin)
