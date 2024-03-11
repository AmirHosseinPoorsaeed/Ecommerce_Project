from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Prefetch

from .models import Product, Attribute, OptionGroup
from store.qas.models import Question, Answer
from store.comments.models import Comment
from store.comments.forms import CommentForm
from store.qas.forms import QuestionForm, AnswerForm


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
              'comments',
              queryset=Comment.objects.select_related('author')
            ),
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
            ),
            Prefetch(
                'product_questions',
                queryset=Question.objects.select_related('author').prefetch_related(
                    Prefetch(
                        'question_answers',
                        queryset=Answer.objects.select_related('author')
                    )
                )
            )
        )
        return product_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['question_form'] = QuestionForm()
        context['answer_form'] = AnswerForm()
        return context
