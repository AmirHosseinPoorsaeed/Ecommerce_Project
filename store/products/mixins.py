from django.shortcuts import get_object_or_404

from .models import Category


class CategoryMixin:
    def get_category(self):
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        return category

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        category = self.get_category()
        queryset = category.products.active_with_stock_info()
        if sort in self.allowed_sort_fields:
            queryset = queryset.order_by(sort)
        return queryset
