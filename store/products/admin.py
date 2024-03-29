from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from jalali_date import datetime2jalali
from nested_inline.admin import NestedTabularInline, NestedModelAdmin, NestedStackedInline

from .models import Category, IPAddress, Product, ProductImage, Attribute, AttributeType, OptionGroup, OptionGroupValue, ProductHit


class ProductImageInline(NestedTabularInline):
    model = ProductImage
    fields = ('image', 'image_preview',)
    readonly_fields = ('image_preview',)
    extra = 0
    min_num = 1

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .select_related('product')


class OptionGroupValueInline(NestedStackedInline):
    model = OptionGroupValue
    fields = ('description',)
    extra = 0
    min_num = 1

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .select_related('group__attribute__product')


class OptionGroupInline(NestedStackedInline):
    model = OptionGroup
    fields = ('title',)
    extra = 0
    min_num = 1
    inlines = (OptionGroupValueInline,)

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .select_related('attribute__product')



class AttributeInline(NestedStackedInline):
    model = Attribute
    fields = ('title', 'type',)
    extra = 0
    min_num = 1
    inlines = (OptionGroupInline,)

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .select_related('product')
    

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    list_display = ('id', 'title', 'image_preview', 'get_categories',
                    'is_active', 'count_hits', 'get_created_jalali',)
    list_per_page = 10
    list_editable = ('is_active',)
    list_display_links = ('id', 'title',)
    list_filter = ('created', 'is_active',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title__icontains', 'category__title__icontains',)
    autocomplete_fields = ('category',)
    ordering = ('-created',)
    readonly_fields = ('image_preview',)
    inlines = (
        ProductImageInline,
        AttributeInline
    )

    def get_queryset(self, request):
        return super() \
            .get_queryset(request) \
            .prefetch_related('category', 'hits') \
            .annotate(
                count_hits=Count('hits')
        )

    @admin.display(description='Categories')
    def get_categories(self, product):
        return ', '.join(category.title for category in product.category.all())

    @admin.display(description='Hits', ordering='count_hits')
    def count_hits(self, product):
        return product.count_hits

    @admin.display(description='Datetime Created', ordering='created')
    def get_created_jalali(self, product):
        return datetime2jalali(product.created).strftime('%a, %d %b %Y %H:%M:%S')

    @admin.display(description='Image')
    def image_preview(self, product):
        return mark_safe(f'<img src="{product.main_cover.url}" width="100" height="100" />')

    image_preview.short_description = 'Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_detail', 'image_preview', 'created',)
    list_per_page = 10
    readonly_fields = ('image_preview',)

    def image_preview(self, image):
        return mark_safe(f'<img src="{image.image.url}" width="100" height="100" />')

    image_preview.short_description = 'Image'

    @admin.display(description='Product')
    def product_detail(self, image):
        url = (
            reverse('admin:products_product_change',
                    args=[image.product.id])
        )
        return format_html(f'<a href="{url}">{image.product}</a>')


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ('title', 'slug', 'is_active',)
    list_editable = ('is_active',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(AttributeType)
class AttributeTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'product',)
    list_select_related = ('type', 'product',)
    autocomplete_fields = ('type', 'product',)
    search_fields = ('title',)


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'attribute',)
    list_select_related = ('attribute',)
    autocomplete_fields = ('attribute',)
    search_fields = ('title',)


@admin.register(OptionGroupValue)
class OptionGroupValueAdmin(admin.ModelAdmin):
    list_display = ('group', 'description',)
    list_select_related = ('group',)
    autocomplete_fields = ('group',)


@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address')


@admin.register(ProductHit)
class ProductHitAdmin(admin.ModelAdmin):
    list_display = ('product', 'ip_address', 'get_created_jalali')
    autocomplete_fields = ('product',)

    @admin.display(description='Datetime Created', ordering='created')
    def get_created_jalali(self, product):
        return datetime2jalali(product.created).strftime('%a, %d %b %Y %H:%M:%S')
