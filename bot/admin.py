from django.contrib import admin 
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('created_at',)

admin.site.register(Product, ProductAdmin)