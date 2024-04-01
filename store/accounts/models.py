from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True, region='IR', null=True)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.user.username}`s Profile'

    @property
    def age(self):
        today = timezone.now().today()
        age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return f'{age} yeas old'

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name
