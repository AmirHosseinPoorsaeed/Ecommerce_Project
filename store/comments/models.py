from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='comments', verbose_name=_('product'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comments', verbose_name=_('author'))
    title = models.CharField(_('title'), max_length=256)
    body = models.TextField(_('body'), )
    is_active = models.BooleanField(_('is_active'), default=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    rate = models.IntegerField(_('rate'), default=1, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True, verbose_name=_('likes'))
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_dislikes', blank=True, verbose_name=_('dislikes'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'{self.author} comment for {self.product}'

    @property
    def count_likes(self):
        return self.likes.count()

    @property
    def count_dislikes(self):
        return self.dislikes.count()

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.product.slug])
