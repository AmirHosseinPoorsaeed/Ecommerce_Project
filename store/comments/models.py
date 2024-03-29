from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

User = get_user_model()


class Comment(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    title = models.CharField(max_length=256)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    rate = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    def __str__(self):
        return f'{self.author} comment for {self.product}'

    @property
    def count_likes(self):
        return self.likes.count()

    @property
    def count_dislikes(self):
        return self.dislikes.count()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.product.slug])
