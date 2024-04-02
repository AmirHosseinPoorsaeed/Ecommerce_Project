import requests
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import transaction
from django.db.models import F
from django.contrib import messages

from store.orders.models import Order
from store.inventory.models import Sale, Stock


def payment_process_sandbox_view(request):
    order_id = request.session.get('order_id')

    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = int(toman_total_price) * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json', 
        }
    
    request_data = {
        'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
        'Amount': rial_total_price,
        'Description': f'#{order.order_number}',
        'CallbackURL': request.build_absolute_uri(reverse('payment:callback')),
    }

    response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = response.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
    else:
        messages.error(request, 'Error from zarinpal')
        return redirect('pages:home')
    
def payment_callback_sandbox_view(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)

    toman_total_price = order.get_total_price()
    rial_total_price = int(toman_total_price) * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json", 
        }

        request_data = {
            'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
            'Amount': rial_total_price,
            'Authority': payment_authority,
        }
        
        response = requests.post(
            url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json', 
            data=json.dumps(request_data), 
            headers=request_header
        )

        if 'errors' not in response.json():
            data = response.json()
            payment_code = data['Status']
            
            if payment_code == 100:
                with transaction.atomic():
                    order.is_paid = True
                    order.ref_id = data['RefID']
                    order.zarinpal_data = data

                    order_items = order.items.select_related('product')
                    for order_item in order_items:
                        product = order_item.product
                        quantity_sold = order_item.quantity

                        sale, created = Sale.objects.get_or_create(product=product)

                        Sale.objects.filter(product=product).update(num_sold=F('num_sold') + quantity_sold)
                        Stock.objects.filter(product=product).update(num_stock=F('num_stock') - quantity_sold)
                    order.save()

                    messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
                    return redirect('pages:home')
            
            elif payment_code == 101:
                messages.warning(request, 'پرداخت شما با موفقیت انجام شد. این تراکنش قبلا ثبت شده است.')
                return redirect('pages:home')
            
            else:
                error_code = response.json()['errors']['code']
                error_message = response.json()['errors']['message']
                messages.error(request, f'تراکنش ناموفق بود {error_message} {error_code}')
                return redirect('pages:home')
    else:
        messages.error(request, 'تراکنش ناموفق بود')
        return redirect('pages:home')
