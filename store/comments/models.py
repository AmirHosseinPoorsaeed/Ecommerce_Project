from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from store.products.models import Product

User = get_user_model()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    title = models.CharField(max_length=256)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    rate = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)

    def __str__(self):
        return f'{self.author} comment for {self.product}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.product.slug])
