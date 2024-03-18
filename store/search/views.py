from django.shortcuts import render
from django.views import generic
from django.contrib.postgres.search import SearchVector

from store.products.models import Product
from store.products.mixins import SortMixin


class SearchListView(SortMixin, generic.ListView):
    template_name = 'search/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        q = self.request.GET.get('q')

        queryset = Product.objects.active_with_stock_info()
        queryset = queryset.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search=q)
        return queryset
