from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import QuestionForm, AnswerForm
from .models import Question
from store.products.models import Product


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = QuestionForm
    template_name = 'qas/question_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        obj.product = product

        return super().form_valid(form)


class AnswerCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = AnswerForm
    template_name = 'qas/answer_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        obj.question = question

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        context['question'] = question
        return context
