from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from store.cart.cart import Cart
from .forms import ShppingForm, AddressForm


@login_required
def shipping_create_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('products:list')

    if request.method == 'POST':
        shipping_form = ShppingForm(request.POST, user=request.user)
        address_form = AddressForm(request.POST)

        if shipping_form.is_valid() and address_form.is_valid():
            address_obj = address_form.save(commit=False)
            address_obj.user = request.user
            address_obj.save()

            shipping_obj = shipping_form.save(commit=False)
            shipping_obj.address = address_obj
            shipping_obj.save()

            request.session['shipping_id'] = shipping_obj.id

            return redirect('orders:create')

        elif shipping_form.is_valid():
            shipping_obj = shipping_form.save(commit=False)

            shipping_obj.save()

            request.session['shipping_id'] = shipping_obj.id

            return redirect('orders:create')

    else:
        shipping_form = ShppingForm(user=request.user)
        address_form = AddressForm()

    return render(request, 'shipping/create.html', {
        'shipping_form': shipping_form,
        'address_form': address_form,
    })
