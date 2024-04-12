from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _

from store.cart.cart import Cart
from .forms import ShppingForm, AddressForm


@login_required
def shipping_create_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('Your cart is empty please add product to cart.'))
        return redirect('products:list')

    if request.method == 'POST':
        shipping_form = ShppingForm(request.POST, user=request.user)
        address_form = AddressForm(request.POST)

        if shipping_form.is_valid():
            shipping_obj = shipping_form.save(commit=False)

            shipping_obj.save()

            request.session['shipping_id'] = shipping_obj.id

            messages.success(request, _('Your shipping successfully saved.'))

            return redirect('orders:create')

    else:
        shipping_form = ShppingForm(user=request.user)
        address_form = AddressForm()

    return render(request, 'shipping/create.html', {
        'shipping_form': shipping_form,
        'address_form': address_form,
    })


class AddressCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = AddressForm
    success_url = reverse_lazy('shipping:create')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user

        messages.success(self.request, _('Your address successfully saved.'))

        return super().form_valid(form)
