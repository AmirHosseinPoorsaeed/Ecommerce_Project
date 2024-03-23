from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import date2jalali

from .models import Shipping, Address, TimeSlot


class ShippingAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('delivery_time_slot', 'max_capacity', 'get_created_jalali',)

    @admin.display(description='تاریخ ایجاد')
    def get_created_jalali(self, obj):
        return date2jalali(obj.delivery_date).strftime('%d %b %Y')


admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Address)
admin.site.register(TimeSlot)
