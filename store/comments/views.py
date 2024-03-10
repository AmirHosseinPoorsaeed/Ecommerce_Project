from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CommentForm
from store.products.models import Product


class CommentCreateView(generic.CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        obj.product = product

        return super().form_valid(form)
