from .forms import SortForm


class SortMixin:
    form_class = SortForm
    allowed_sort_fields = ('sale_price', '-sale_price', '-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = self.form_class
        return context

    def get_sorted_queryset(self, queryset):
        sort = self.request.GET.get('sort')
        if sort in self.allowed_sort_fields:
            queryset = queryset.order_by(sort)
        return queryset
