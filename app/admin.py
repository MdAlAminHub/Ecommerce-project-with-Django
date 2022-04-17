from django.contrib import admin
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    Stock,
)
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'Zipcode', 'state']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_stock','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'qunatity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'qunatity', 'ordered_date', 'status']


@admin.register(Stock)
class StockModelAdmin(admin.ModelAdmin):
    list_display = ['sold_quantity', 'product', 'stock_available']

