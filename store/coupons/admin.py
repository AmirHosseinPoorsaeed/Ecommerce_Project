from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('code', 'get_created_jalali', 'get_expired_jalali', 'discount', 'active',)

    @admin.display(description='تاریخ ایجاد')
    def get_created_jalali(self, obj):
		    return datetime2jalali(obj.valid_from).strftime('%a, %d %b %Y %H:%M:%S')
    
    @admin.display(description='تاریخ انقضاء')
    def get_expired_jalali(self, obj):
		    return datetime2jalali(obj.valid_to).strftime('%a, %d %b %Y %H:%M:%S')

