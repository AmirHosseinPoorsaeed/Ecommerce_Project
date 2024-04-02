from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse

from jalali_date import datetime2jalali

from .models import Order, OrderItem


def order_pdf(obj):
    if obj.is_paid:
        url = reverse('orders:order_pdf', args=[obj.order_number])
        return mark_safe(f'<a href="{url}">PDF</a>')
    return


order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'quantity', 'price',)
    autocomplete_fields = ('product',)
    extra = 0
    min_num = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('shipping', 'coupon_detail', 'is_paid',
                    'get_created_jalali', order_pdf)
    list_filter = ('is_paid', 'created',)
    list_per_page = 10
    search_fields = ('user__first_name__icontains',)
    autocomplete_fields = ('shipping', 'user',)
    ordering = ('-created',)
    inlines = (
        OrderItemInline,
    )

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .select_related('coupon', 'user', 'shipping__address')

    @admin.display(description='Datetime Created', ordering='created')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='Coupon')
    def coupon_detail(self, order):
        if order.coupon:
            url = (
                reverse('admin:coupons_coupon_change', args=[order.coupon.id])
            )
            return format_html(f'<a href="{url}">Coupon</a>')
        return 'No Coupon'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_detail', 'quantity', 'price',)
    list_editable = ('quantity',)
    list_per_page = 10
    autocomplete_fields = ('order', 'product',)

    @admin.display(description='Product')
    def product_detail(self, order_item):
        url = (
            reverse('admin:products_product_change',
                    args=[order_item.product.id])
        )
        return format_html(f'<a href="{url}">{order_item.product}</a>')
