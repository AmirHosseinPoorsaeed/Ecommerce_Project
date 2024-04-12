from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TimeStampedModel(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    text = models.TextField(_('text'), )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='questions', verbose_name=_('author'))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='product_questions', verbose_name=_('product'))
    is_active = models.BooleanField(_('is_active'), default=True)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return f'{self.text} --> {self.author.first_name}'

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.product.slug])


class Answer(TimeStampedModel):
    text = models.TextField(_('text'), )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='answers', verbose_name=_('author'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers', verbose_name=_('question'))

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self):
        return f'{self.author.first_name} answer'

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.question.product.slug])
