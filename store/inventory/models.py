from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Stock(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='stock_records', verbose_name=_('product'))
    sku = models.CharField(_('sku'), max_length=256, blank=True, unique=True)
    buy_price = models.PositiveBigIntegerField(_('buy_price'), null=True, blank=True)
    sale_price = models.PositiveBigIntegerField(_('sale_price'), )
    discount = models.PositiveIntegerField(_('discount'), validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ], blank=True, null=True)
    num_stock = models.PositiveIntegerField(_('num_stock'), default=0)
    threshold_low_stock = models.PositiveIntegerField(_('threshold_low_stock'), null=True, blank=True)

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

    def __str__(self):
        return self.sku

    @property
    def final_price(self):
        if self.discount:
            return int(self.sale_price - (self.sale_price * self.discount / 100))
        return self.sale_price

    
class Sale(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='sale_records', verbose_name=_('product'))
    num_sold = models.PositiveIntegerField(_('num_sold'), default=0)
    sold_at = models.DateTimeField(_('sold_at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')

    def __str__(self):
        return f'{self.product}'
