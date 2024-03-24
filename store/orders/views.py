from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings

import weasyprint
import os

from store.cart.cart import Cart
from store.shipping.models import Shipping
from .forms import OrderForm
from .models import OrderItem, Order


def order_create_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('products:list')

    shipping_id = request.session.get('shipping_id')

    shipping = get_object_or_404(Shipping, id=shipping_id)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            if cart.coupon:
                order_obj.coupon = cart.coupon
                order_obj.discount = cart.coupon.discount
            order_obj.user = request.user
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

            return redirect('pages:home')

    else:
        order_form = OrderForm()

    return render(request, 'orders/create.html', {
        'shipping': shipping,
        'order_form': order_form,
    })


def order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(os.path.join(settings.STATICFILES_DIRS[0], 'css\pdf.css'))
    ])
    return response
