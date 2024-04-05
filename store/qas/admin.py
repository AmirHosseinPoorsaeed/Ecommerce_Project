from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.db.models import Count

from jalali_date import datetime2jalali

from .models import Question, Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    fields = ('text', 'author',)
    extra = 0
    autocomplete_fields = ('author',)

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .select_related('author',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'author_detail', 'product_detail',
                    'is_active', 'count_answers', 'get_created_jalali',)
    list_per_page = 10
    list_filter = ('created', 'is_active',)
    ordering = ('-created',)
    list_editable = ('is_active',)
    autocomplete_fields = ('product', 'author',)
    search_fields = ('text__icontains',)
    inlines = (
        AnswerInline,
    )

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .prefetch_related('question_answers',) \
            .select_related('author', 'product') \
            .annotate(count_answers=Count('question_answers'))

    @admin.display(description='Datetime Created', ordering='created')
    def get_created_jalali(self, question):
        return datetime2jalali(question.created).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='Product')
    def product_detail(self, question):
        url = (
            reverse('admin:products_product_change',
                    args=[question.product.id])
        )
        return format_html(f'<a href="{url}">{question.product}</a>')

    @admin.display(description='Author')
    def author_detail(self, question):
        url = (
            reverse('admin:accounts_customuser_change',
                    args=[question.author.id])
        )
        return format_html(f'<a href="{url}">{question.author}</a>')

    @admin.display(description='Answers')
    def count_answers(self, question):
        url = (
            reverse('admin:qas_answer_changelist')
            + '?'
            + urlencode({
                'question__id': question.id,
            })
        )

        return format_html(f'<a href="{url}">{question.count_answers}</a>')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'author_detail', 'get_created_jalali',)
    list_per_page = 10
    list_filter = ('created',)
    autocomplete_fields = ('author', 'question',)
    search_fields = ('text__icontains', 'author__icontains',
                     'question__icontains',)
    ordering = ('-created',)

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .select_related('author')

    @admin.display(description='Datetime Created', ordering='created')
    def get_created_jalali(self, answer):
        return datetime2jalali(answer.created).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='Author')
    def author_detail(self, answer):
        url = (
            reverse('admin:accounts_customuser_change',
                    args=[answer.author.id])
        )
        return format_html(f'<a href="{url}">{answer.author}</a>')
