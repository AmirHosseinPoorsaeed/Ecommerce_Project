from django.utils import timezone

from celery import shared_task

from .models import Coupon


@shared_task
def update_coupon_status():
    current_time = timezone.now()
    tehran_now = current_time.astimezone(timezone.get_current_timezone())

    coupons_to_deactivate = Coupon.objects.filter(
        valid_to__lt=tehran_now,
        active=True
    )
    
    updated_coupons = []

    for coupon in coupons_to_deactivate:
        coupon.active = False
        updated_coupons.append(coupon)

    Coupon.objects.bulk_update(updated_coupons, ['active'])
