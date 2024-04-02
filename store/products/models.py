from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings

from treebeard.mp_tree import MP_Node

from .managers import ProductManager



class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()

    class Meta:
        verbose_name = 'IP Address'
        verbose_name_plural = 'IP Addresses'

    def __str__(self):
        return self.ip_address


class Category(MP_Node):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title


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
    hits = models.ManyToManyField(IPAddress, through='ProductHit', blank=True, related_name='hits')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ProductFavorite', blank=True, related_name='favorites')

    objects = ProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])
    

class ProductFavorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
        

class ProductHit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class ProductImage(TimeStampedModel):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='users/%Y/%m/%d/')

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f'{self.product.title}  -->  {self.image}'
    
    def image_preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')
    
    image_preview.short_description = 'Image'


class AttributeType(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Attribute Type'
        verbose_name_plural = 'Attribute Types'
    
    def __str__(self):
        return self.title



class Attribute(models.Model):
    title = models.CharField(max_length=256)
    type = models.ForeignKey('products.AttributeType', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='attributes')

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
    
    def __str__(self):
        return f'Attribute {self.product.title}: {self.title}'


class OptionGroup(models.Model):
    title = models.CharField(max_length=256)
    attribute = models.ForeignKey('products.Attribute', on_delete=models.CASCADE, related_name='options')

    class Meta:
        verbose_name = 'Option Group'
        verbose_name_plural = 'Option Groups'

    def __str__(self):
        return f'Option {self.attribute.title}: {self.title}'


class OptionGroupValue(models.Model):
    description = models.CharField(max_length=512)
    group = models.ForeignKey('products.OptionGroup', on_delete=models.CASCADE, related_name='values')

    class Meta:
        verbose_name = 'Option Group Value'
        verbose_name_plural = 'Option Group Values'

    def __str__(self):
        return f'Value {self.group.title}: {self.description}'
