from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order


def order_pdf(obj):
    url = reverse('orders:order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_paid', order_pdf]
