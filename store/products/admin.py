from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Category, Product, ProductImage, Attribute, AttributeType, OptionGroup, OptionGroupValue, ProductHit

admin.site.register(ProductImage)
admin.site.register(Attribute)
admin.site.register(AttributeType)
admin.site.register(OptionGroup)
admin.site.register(OptionGroupValue)


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(ProductHit)
class ProductHitAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryAdmin)
