from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Stock(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='stock_records')
    sku = models.CharField(max_length=256, blank=True, unique=True)
    buy_price = models.PositiveBigIntegerField(null=True, blank=True)
    sale_price = models.PositiveBigIntegerField()
    discount = models.PositiveIntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ], blank=True, null=True)
    num_stock = models.PositiveIntegerField(default=0)
    threshold_low_stock = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return self.sku

    @property
    def final_price(self):
        if self.discount:
            return int(self.sale_price - (self.sale_price * self.discount / 100))
        return self.sale_price

    
class Sale(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='sale_records')
    num_sold = models.PositiveIntegerField(default=0)
    sold_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        return f'{self.product}'
