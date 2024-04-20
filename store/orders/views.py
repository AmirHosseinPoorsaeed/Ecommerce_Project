from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

import weasyprint
import os

from store.cart.cart import Cart
from store.shipping.models import Shipping
from .forms import OrderForm
from .models import OrderItem, Order


@login_required
def order_create_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('Your cart is empty please add product to cart.'))
        return redirect('products:list')

    shipping_id = request.session.get('shipping_id')

    shipping = get_object_or_404(Shipping, id=shipping_id)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            with transaction.atomic():
                order_obj = order_form.save(commit=False)
                if cart.coupon:
                    order_obj.coupon = cart.coupon
                    order_obj.discount = cart.coupon.discount
                    del request.session['coupon_id']
                order_obj.user = request.user.customer
                order_obj.shipping = shipping
                order_obj.save()

                order_items = (
                    OrderItem(
                        order=order_obj,
                        product=cart_item['product_obj'],
                        quantity=cart_item['quantity'],
                        price=cart_item['price'],
                    )
                    for cart_item in cart
                )

                OrderItem.objects.bulk_create(order_items)

                cart.clear()

                request.user.first_name = shipping.address.receiver_first_name
                request.user.last_name = shipping.address.receiver_last_name
                request.user.save()

                request.session['order_id'] = order_obj.id

                del request.session['shipping_id']

                messages.success(request, _('Order successfully created.'))

                return redirect('payment:process')

    else:
        order_form = OrderForm()

    return render(request, 'orders/create.html', {
        'shipping': shipping,
        'order_form': order_form,
    })


def order_pdf(request, order_id):
    order = get_object_or_404(Order, order_number=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(os.path.join(settings.STATICFILES_DIRS[0], 'css\pdf.css'))
    ])
    return response


class CustomerOrderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.customer) \
            .select_related('shipping', 'user') \
            .prefetch_related('items') \
            .annotate(address=F('shipping__address__address')) \
            .order_by('-created')
