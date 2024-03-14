from django.db.models import F, Prefetch, Count, Avg, Manager, ExpressionWrapper, FloatField

from store.comments.models import Comment
from store.qas.models import Question, Answer


class ProductManager(Manager):
    def active_with_stock_info(self):
        return self.filter(is_active=True).prefetch_related(
            'stock_records'
        ).annotate(
            num_stock=F('stock_records__num_stock'),
            sale_price=F('stock_records__sale_price'),
            threshold_low_stock=F('stock_records__threshold_low_stock'),
            discount=F('stock_records__discount'),
            final_price=(
                F('stock_records__sale_price') - (
                    F('stock_records__sale_price') * F('stock_records__discount') / 100
                )
            )
        )

    def with_related_info(self, slug):
        from .models import Attribute, OptionGroup
        return self.filter(slug=slug).prefetch_related(
            'stock_records',
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
        ).annotate(
            num_stock=F('stock_records__num_stock'),
            sale_price=F('stock_records__sale_price'),
            threshold_low_stock=F('stock_records__threshold_low_stock'),
            sku=F('stock_records__sku'),
            comment_count=Count('comments'),
            average_rate=Avg('comments__rate'),
            discount=F('stock_records__discount'),
            final_price=(
                F('stock_records__sale_price') - (
                    F('stock_records__sale_price') * F('stock_records__discount') / 100
                )
            )
        )
