from django.contrib import admin
from ads.models import Product, Customer, Order, Discount


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('for_every_qty_items',
                    'free_items',
                    'fixed_discount',
                    'min_qty_before_fixed_discount',)
