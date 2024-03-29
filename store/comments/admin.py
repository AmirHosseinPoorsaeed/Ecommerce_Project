from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from jalali_date import datetime2jalali

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_detail', 'author_detail', 'title', 'rate',
                    'count_likes', 'count_dislikes', 'is_active', 'get_created_jalali',)
    list_filter = ('created', 'is_active',)
    list_editable = ('is_active',)
    list_per_page = 10
    autocomplete_fields = ('product', 'author', 'likes', 'dislikes',)
    search_fields = ('title__icontains', 'body__icontains',)

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .prefetch_related('likes', 'dislikes') \
            .select_related('author', 'product')

    @admin.display(description='Datetime Created', ordering='created')
    def get_created_jalali(self, comment):
        return datetime2jalali(comment.created).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='Count Likes', ordering='likes')
    def count_like(self, comment):
        return comment.likes.count()

    @admin.display(description='Count Dislikes', ordering='dislikes')
    def count_dislike(self, comment):
        return comment.dislikes.count()

    @admin.display(description='Product')
    def product_detail(self, comment):
        url = (
            reverse('admin:products_product_change',
                    args=[comment.product.id])
        )
        return format_html(f'<a href="{url}">{comment.product}</a>')

    @admin.display(description='Author')
    def author_detail(self, comment):
        url = (
            reverse('admin:accounts_customuser_change',
                    args=[comment.author.id])
        )
        return format_html(f'<a href="{url}">{comment.author}</a>')
