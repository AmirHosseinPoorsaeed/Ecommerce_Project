import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    building_number = models.PositiveSmallIntegerField()
    unit = models.PositiveSmallIntegerField(blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    receiver_first_name = models.CharField(max_length=64)
    receiver_last_name = models.CharField(max_length=64)
    mobile = PhoneNumberField(region='IR')

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'

    def __str__(self):
        return f'{self.start_time} to {self.end_time}'


class Shipping(models.Model):
    address = models.ForeignKey('shipping.Address', on_delete=models.PROTECT)
    delivery_date = models.DateField()
    delivery_time_slot = models.ForeignKey('shipping.TimeSlot', on_delete=models.PROTECT)
    max_capacity = models.PositiveSmallIntegerField(default=10)

    class Meta:
        verbose_name = 'Shipping'
        verbose_name_plural = 'Shippings'

    def clean(self):
        if not self.time_slot_is_available():
            raise ValidationError('The selected time slot is not available.')

    def time_slot_is_available(self):
        existing_shipments = Shipping.objects.filter(
            delivery_date=self.delivery_date,
            delivery_time_slot=self.delivery_time_slot
        )
        return existing_shipments.count() < self.max_capacity


# class Order(models.Model):
#     order_number = models.UUIDField(default=uuid.uuid4().hex)
#     shipping = models.ForeignKey('store.shipping.Shipping', on_delete=models.PROTECT)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
#     is_paid = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = 'Order'
#         verbose_name_plural = 'Orders'
#
#     def get_total_price(self):
#         return sum(item.quantity * item.price for item in self.items.all())
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey('store.shipping.Order', on_delete=models.PROTECT, related_name='items')
#     product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items')
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name = 'Order Item'
#         verbose_name_plural = 'Order Items'
