from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Product
from store.comments.forms import CommentForm
from store.qas.forms import QuestionForm, AnswerForm
from .mixins import CategoryMixin


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return Product.objects.active_with_stock_info()


class CategoryListView(CategoryMixin, generic.ListView):
    template_name = 'products/category_list.html'
    context_object_name = 'products'
    paginate_by = 1


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
