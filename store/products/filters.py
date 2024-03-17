import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'stock_records__sale_price': ['lte', 'gte'],
        }
