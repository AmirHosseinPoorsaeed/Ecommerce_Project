from django.contrib import admin
from django.db.models import Count

from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import date2jalali

from .models import Shipping, Address, TimeSlot


@admin.register(Shipping)
class ShippingAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('address', 'delivery_time_slot', 'get_created_jalali', 'max_capacity',)
    ordering = ('delivery_date',)
    search_fields = ('address__address__icontains',)

    @admin.display(description='Datetime Created', ordering='delivery_date')
    def get_created_jalali(self, obj):
        return date2jalali(obj.delivery_date).strftime('%d %b %Y')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'postal_code', 'mobile', 'counts_shipping',)

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .prefetch_related('shippings') \
            .annotate(count_shipping=Count('shippings'))

    @admin.display(description='Count Shippings', ordering='count_shipping')
    def counts_shipping(self, address):
        return address.count_shipping


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time')
