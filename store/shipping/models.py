from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    address = models.TextField(_('address'))
    city = models.CharField(_('city'), max_length=64)
    province = models.CharField(_('province'), max_length=64)
    building_number = models.PositiveSmallIntegerField(_('building_number'))
    unit = models.PositiveSmallIntegerField(_('unit'), blank=True, null=True)
    postal_code = models.CharField(_('postal_code'), max_length=10)
    receiver_first_name = models.CharField(_('receiver_first_name'), max_length=64)
    receiver_last_name = models.CharField(_('receiver_last_name'), max_length=64)
    mobile = PhoneNumberField(_('mobile'), region='IR')

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'Address: {self.address}'


class TimeSlot(models.Model):
    start_time = models.TimeField(_('start_time'))
    end_time = models.TimeField(_('end_time'))

    class Meta:
        verbose_name = _('Time Slot')
        verbose_name_plural = _('Time Slots')

    def __str__(self):
        return f'{self.start_time} to {self.end_time}'


class Shipping(models.Model):
    address = models.ForeignKey('shipping.Address', on_delete=models.PROTECT, related_name='shippings', verbose_name=_('address'))
    delivery_date = models.DateField(_('delivery_date'))
    delivery_time_slot = models.ForeignKey('shipping.TimeSlot', on_delete=models.PROTECT, verbose_name=_('delivery_time_slot'))
    max_capacity = models.PositiveSmallIntegerField(_('max_capacity'), default=10)

    class Meta:
        verbose_name = _('Shipping')
        verbose_name_plural = _('Shippings')

    def __str__(self):
        return f'shipping id: {self.id} in {self.delivery_date}, {self.address.address}'

    def clean(self):
        if not self.time_slot_is_available():
            raise ValidationError('The selected time slot is not available.')

    def time_slot_is_available(self):
        existing_shipments = Shipping.objects.filter(
            delivery_date=self.delivery_date,
            delivery_time_slot=self.delivery_time_slot
        )
        return existing_shipments.count() < self.max_capacity
