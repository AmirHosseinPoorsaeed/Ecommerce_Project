from django.db import models
from django.conf import settings


class Order(models.Model):
    shipping = models.ForeignKey('shipping.Shipping', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    note = models.CharField(max_length=200, blank=True)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
