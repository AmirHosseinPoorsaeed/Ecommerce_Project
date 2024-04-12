from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from treebeard.mp_tree import MP_Node

from .managers import ProductManager


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(_('ip_address'))

    class Meta:
        verbose_name = _('IP Address')
        verbose_name_plural = _('IP Addresses')

    def __str__(self):
        return self.ip_address


class Category(MP_Node):
    title = models.CharField(_('title'), max_length=64)
    description = models.CharField(_('description'), max_length=256, blank=True)
    slug = models.SlugField(_('slug'), unique=True, allow_unicode=True)
    is_active = models.BooleanField(_('is_active'), default=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def __str__(self):
        return self.title


class TimeStampedModel(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class Product(TimeStampedModel):
    title = models.CharField(_('title'), max_length=256)
    summary = models.TextField(_('summary'), blank=True)
    description = models.TextField(_('description'), blank=True)
    main_cover = models.ImageField(_('main_cover'), upload_to='cover/%Y/%m/%d/')
    slug = models.SlugField(_('slug'), max_length=256, unique=True, allow_unicode=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    category = models.ManyToManyField(Category, related_name='products', verbose_name=_('category'))
    hits = models.ManyToManyField(IPAddress, through='ProductHit', blank=True, related_name='hits', verbose_name=_('hits'))
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ProductFavorite', blank=True, related_name='favorites', verbose_name=_('favorites'))

    objects = ProductManager()

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])
    

class ProductFavorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name=_('product'))

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = _('Product Favorite')
        verbose_name_plural = _('Products Favorites')
        

class ProductHit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE, verbose_name=_('ip_address'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product Hit')
        verbose_name_plural = _('Products Hits')


class ProductImage(TimeStampedModel):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images', verbose_name=_('product'))
    image = models.ImageField(upload_to='users/%Y/%m/%d/', verbose_name=_('image'))

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

    def __str__(self):
        return f'{self.product.title}  -->  {self.image}'
    
    def image_preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')
    
    image_preview.short_description = 'Image'


class AttributeType(models.Model):
    title = models.CharField(_('title'), max_length=256)

    class Meta:
        verbose_name = _('Attribute Type')
        verbose_name_plural = _('Attribute Types')
    
    def __str__(self):
        return self.title



class Attribute(models.Model):
    title = models.CharField(_('title'), max_length=256)
    type = models.ForeignKey('products.AttributeType', on_delete=models.CASCADE, verbose_name=_('type'))
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='attributes', verbose_name=_('product'))

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')
    
    def __str__(self):
        return f'Attribute {self.product.title}: {self.title}'


class OptionGroup(models.Model):
    title = models.CharField(_('title'), max_length=256)
    attribute = models.ForeignKey('products.Attribute', on_delete=models.CASCADE, related_name='options', verbose_name=_('attribute'))

    class Meta:
        verbose_name = _('Option Group')
        verbose_name_plural = _('Option Groups')

    def __str__(self):
        return f'Option {self.attribute.title}: {self.title}'


class OptionGroupValue(models.Model):
    description = models.CharField(_('description'), max_length=512)
    group = models.ForeignKey('products.OptionGroup', on_delete=models.CASCADE, related_name='values', verbose_name=_('group'))

    class Meta:
        verbose_name = _('Option Group Value')
        verbose_name_plural = _('Option Group Values')

    def __str__(self):
        return f'Value {self.group.title}: {self.description}'
