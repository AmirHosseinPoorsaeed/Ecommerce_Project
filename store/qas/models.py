from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='questions')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='product_questions')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'{self.text} --> {self.author.first_name}'

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.product.slug])


class Answer(TimeStampedModel):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f'{self.author.first_name} answer'

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.question.product.slug])
