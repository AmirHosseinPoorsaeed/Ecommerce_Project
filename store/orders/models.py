from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    shipping = models.ForeignKey('shipping.Shipping', on_delete=models.PROTECT, verbose_name=_('shipping'))
    user = models.ForeignKey('accounts.Customer', on_delete=models.PROTECT, verbose_name=_('user'))
    order_number = models.UUIDField(_('order_number'), unique=True, default=uuid4, editable=False)
    note = models.CharField(_('note'), max_length=200, blank=True)
    is_paid = models.BooleanField(_('is_paid'), default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    coupon = models.ForeignKey(
        'coupons.Coupon', 
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True,
        null=True,
        verbose_name=_('coupon'))
    discount = models.IntegerField(_('discount'), default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])

    zarinpal_authority = models.CharField(_('zarinpal_authority'), max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(_('zarinpal_ref_id'), max_length=255, blank=True)
    zarinpal_data = models.TextField(_('zarinpal_data'), blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order id={self.id} for {self.user.first_name}'

    def get_total_price_before_discount(self):
        return sum(item.quantity * item.price for item in self.items.all())

    def get_discount(self):
        total_price = self.get_total_price_before_discount()
        if self.discount:
            return round(total_price * (self.discount / Decimal(100)), 0)
        return Decimal(0)
    
    def get_total_price(self):
        total_price = self.get_total_price_before_discount()
        return round(total_price - self.get_discount(), 0)


class OrderItem(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price = models.PositiveIntegerField(_('price'))

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items' )

    def get_price(self):
        return self.price * self.quantity
