from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Order(models.Model):
    shipping = models.ForeignKey('shipping.Shipping', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    note = models.CharField(max_length=200, blank=True)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(
        'coupons.Coupon', 
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True,
        null=True)
    discount = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])

    zarinpal_authority = models.CharField(max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(max_length=255, blank=True)
    zarinpal_data = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

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
    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def get_price(self):
        return self.price * self.quantity
