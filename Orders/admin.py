from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

#Model Order being registered
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'tableNo', 'order_placed_at', 'notes', 'status', 'total_price', 'customer_name', 'delivered_at')
    search_fields = ('orderID',)
    list_filter = ('order_placed_at',)
    
#Model Order Item being registered
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'foodID', 'drinkID', 'price')
    search_fields = ('orderID',)