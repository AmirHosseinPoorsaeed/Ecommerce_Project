from django.contrib import admin
from django.utils import timezone

from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('code', 'discount', 'get_created_jalali', 'get_expired_jalali', 'days_left', 'active',)
    list_filter = ('active', 'valid_to',)
    list_per_page = 10
    ordering = ('-valid_to',)

    def days_left(self, coupon):
        today = timezone.now()
        if coupon.valid_to > today:
            return (coupon.valid_to - today).days
        return 0
    
    @admin.display(description='Datetime Created')
    def get_created_jalali(self, coupon):
        return datetime2jalali(coupon.valid_from).strftime('%a, %d %b %Y %H:%M:%S')
    
    @admin.display(description='Datetime Expired')
    def get_expired_jalali(self, coupon):
        return datetime2jalali(coupon.valid_to).strftime('%a, %d %b %Y %H:%M:%S')




