from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import CommentForm
from .models import Comment
from store.products.models import Product


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        obj.product = product

        messages.success(self.request, _('Comment successfully saved.'))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        
        context['product'] = product
        return context


@login_required
def comment_like(request, comment_id, reaction):
    comment = get_object_or_404(Comment, pk=comment_id)

    if reaction == 'like':
        reaction_set = comment.likes
        other_reaction_set = comment.dislikes
    elif reaction == 'dislike':
        reaction_set = comment.dislikes
        other_reaction_set = comment.likes
    else:
        return redirect(comment.get_absolute_url())

    if request.user in reaction_set.all():
        reaction_set.remove(request.user)
        messages.success(request, _('Your like successfully saved.'))
    elif request.user in other_reaction_set.all():
        reaction_set.add(request.user)
        other_reaction_set.remove(request.user)
        messages.success(request, _('Your dislike successfully saved.'))
    else:
        reaction_set.add(request.user)
        messages.success(request, _('Your like successfully saved.'))

    return redirect(comment.get_absolute_url())
