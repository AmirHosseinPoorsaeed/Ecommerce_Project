from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def apply_coupon(request):
    utc_now = timezone.now()
    tehran_now = utc_now.astimezone(timezone.get_current_timezone())
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=tehran_now,
                valid_to__gte=tehran_now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
        
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    
    return redirect('cart:detail')
