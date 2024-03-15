from django.shortcuts import render, get_object_or_404
from django.views import generic

from store.comments.forms import CommentForm
from store.qas.forms import QuestionForm, AnswerForm
from .models import Product
from .mixins import CategoryMixin
from .forms import SortForm


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    form_class = SortForm
    allowed_sort_fields = ('sale_price', '-sale_price', '-created')

    def get_queryset(self):
        queryset = Product.objects.active_with_stock_info()
        sort = self.request.GET.get('sort')
        if sort in self.allowed_sort_fields:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = self.form_class
        return context


class CategoryListView(CategoryMixin, generic.ListView):
    template_name = 'products/category_list.html'
    context_object_name = 'products'
    paginate_by = 10
    form_class = SortForm
    allowed_sort_fields = ('sale_price', '-sale_price', '-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = self.form_class
        return context


class ProductDetailView(generic.DetailView):
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        product_slug = self.kwargs.get('slug')
        return Product.objects.with_related_info(product_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['question_form'] = QuestionForm()
        context['answer_form'] = AnswerForm()
        return context
