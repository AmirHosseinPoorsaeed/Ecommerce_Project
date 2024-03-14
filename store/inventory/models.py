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

    def __str__(self):
        return self.sku

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'




