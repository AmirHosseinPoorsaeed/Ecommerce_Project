from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from jalali_date import datetime2jalali

from .models import Stock, Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_detail', 'num_sold', 'get_created_jalali',)
    list_filter = ('sold_at',)
    ordering = ('-sold_at', '-num_sold')
    list_select_related = ('product',)

    @admin.display(description='Datetime Sold', ordering='sold_at')
    def get_created_jalali(self, sale):
        return datetime2jalali(sale.sold_at).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='Product')
    def product_detail(self, sale):
        url = (
            reverse('admin:products_product_change',
                    args=[sale.product.id])
        )
        return format_html(f'<a href="{url}">{sale.product}</a>')


class StockFilter(admin.SimpleListFilter):
    LESS_THAN_10 = '<10'
    BETWEEN_10_AND_50 = '10<=50'
    MORE_THAN_50 = '>50'
    title = 'Critical Stock Status'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return (
            (StockFilter.LESS_THAN_10, 'High'),
            (StockFilter.BETWEEN_10_AND_50, 'Medium'),
            (StockFilter.MORE_THAN_50, 'OK'),
        )

    def queryset(self, request, queryset):
        if self.value() == StockFilter.LESS_THAN_10:
            return queryset.filter(num_stock__lt=10)
        if self.value() == StockFilter.BETWEEN_10_AND_50:
            return queryset.filter(num_stock__range=(10, 50))
        if self.value() == StockFilter.MORE_THAN_50:
            return queryset.filter(num_stock__gt=50)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product_detail', 'buy_price',
                    'sale_price', 'discount', 'num_stock', 'stock_status',)
    list_per_page = 10
    list_editable = ('discount', 'sale_price',)
    list_select_related = ('product',)
    search_fields = ('product__icontains', 'sku__icontains',)
    autocomplete_fields = ('product',)
    list_filter = (StockFilter,)

    @admin.display(description='Product')
    def product_detail(self, stock):
        url = (
            reverse('admin:products_product_change',
                    args=[stock.product.id])
        )
        return format_html(f'<a href="{url}">{stock.product}</a>')
    
    @admin.display(description='Status')
    def stock_status(self, stock):
        if stock.num_stock < 10:
            return 'Low'
        if stock.num_stock > 50:
            return 'High'
        return 'Medium'
