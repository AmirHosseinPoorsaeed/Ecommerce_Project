from django.shortcuts import get_object_or_404

from .models import Category


class CategoryMixin:
    def get_category(self):
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        return category

    def get_queryset(self):
        category = self.get_category()
        return category.products.active_with_stock_info()
