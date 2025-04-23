from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'stock_quantity',
        'price',
        'featured',
        'image',
    )

    list_filter = ('featured',)
    search_fields = ('name', 'sku', 'description')
    ordering = ('sku',)


admin.site.register(Product, ProductAdmin)
