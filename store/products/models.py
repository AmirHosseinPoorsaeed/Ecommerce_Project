from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from treebeard.mp_tree import MP_Node

from .managers import ProductManager


class Category(MP_Node):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(TimeStampedModel):
    title = models.CharField(max_length=256)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    main_cover = models.ImageField(upload_to='cover/%Y/%m/%d/')
    slug = models.SlugField(max_length=256, unique=True, allow_unicode=True)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, related_name='products')

    objects = ProductManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(TimeStampedModel):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='users/%Y/%m/%d/')

    def __str__(self):
        return f'{self.product}  -->  {self.image}'

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class AttributeType(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Attribute Type'
        verbose_name_plural = 'Attribute Types'


class Attribute(models.Model):
    title = models.CharField(max_length=256)
    type = models.ForeignKey('products.AttributeType', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='attributes')

    def __str__(self):
        return f'{self.title} --> {self.product}'

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'


class OptionGroup(models.Model):
    title = models.CharField(max_length=256)
    attribute = models.ForeignKey('products.Attribute', on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return f'{self.title} --> {self.attribute}'

    class Meta:
        verbose_name = 'Option Group'
        verbose_name_plural = 'Option Groups'


class OptionGroupValue(models.Model):
    description = models.CharField(max_length=512)
    group = models.ForeignKey('products.OptionGroup', on_delete=models.CASCADE, related_name='values')

    def __str__(self):
        return f'{self.description} --> {self.group}'

    class Meta:
        verbose_name = 'Option Group Value'
        verbose_name_plural = 'Option Group Values'
