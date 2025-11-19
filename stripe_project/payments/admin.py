from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency']
    list_filter = ['currency']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_amount', 'created_at']
    inlines = [OrderItemInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent_off', 'order']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'percentage', 'order']