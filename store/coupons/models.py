from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    code = models.CharField(_('code'), max_length=50, unique=True)
    valid_from = models.DateTimeField(_('valid_from'), )
    valid_to = models.DateTimeField(_('valid_to'), )
    discount = models.IntegerField(_('discount'), validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    active = models.BooleanField(_('active'), )

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def __str__(self):
        return self.code
