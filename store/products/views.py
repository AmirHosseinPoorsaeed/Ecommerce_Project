from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Prefetch

from .models import Product, Attribute, OptionGroup


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.prefetch_related(
            'images',
        ).filter(is_active=True)


class ProductDetailView(generic.DetailView):
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        product_slug = self.kwargs.get('slug')
        product_queryset = Product.objects.filter(slug=product_slug)
        product_queryset = product_queryset.prefetch_related(
            Prefetch(
                'attributes',
                queryset=Attribute.objects.prefetch_related(
                    Prefetch(
                        'options',
                        queryset=OptionGroup.objects.prefetch_related(
                            'values'
                        )
                    )
                )
            )
        )
        return product_queryset

