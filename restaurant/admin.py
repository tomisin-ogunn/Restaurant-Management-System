from django.contrib import admin
from .models import Table, Reservation, Food, Drink, Favourite, Basket, OrderItem, Rating, Order
from .models import KitchenZone

# Register your models here.

# Custom admin class for Table
class TableAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('tableNo', 'capacity', 'waiter', 'status')
    search_fields = ('tableNo', 'capacity', 'waiter', 'status')
    
# Register the Table model with the custom admin class
admin.site.register(Table, TableAdmin)

#Custom admin class for Reservation
class ReservationAdmin(admin.ModelAdmin):
    #Customize fields displayed in the admin list view
    list_display = ('reservationId', 'size', 'comments', 'tableNo', 'startTime', 'endTime', 'duration', 'time_booked', 'customer_name', 'reservation_date')
    search_fields = ('reservationId', 'size', 'comments', 'tableNo', 'startTime', 'endTime', 'duration', 'time_booked', 'customer_name', 'reservation_date')
    
#Register the Reservation model with the custom admin class
admin.site.register(Reservation, ReservationAdmin)

#Custom admin class for the Food Model
class FoodAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('foodId', 'food_name', 'ingredients', 'category', 'duration', 'price', 'image', 'allergen', 'calories')
    search_fields = ('foodId', 'food_name', 'category')
    
#Register the Food Model with the custom admin class
admin.site.register(Food, FoodAdmin)    

#Custom Admin class for the Drink Model
class DrinkAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('drinkId', 'drink_name', 'description', 'alcoholConc', 'price', 'image', 'category', 'calories')
    search_fields = ('drinkId', 'drink_name', 'description', 'price')

#Register the Drink Model with the custom admin class
admin.site.register(Drink, DrinkAdmin)    


#Custom Admin class for the Customer Favourites Model
class FavouriteAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('favourite_id', 'customer_id', 'food_id', 'drink_id')
    search_fields = ('favourite_id', 'customer_id', 'food_id', 'drink_id')

#Register the Favourites Model with the custom admin class
admin.site.register(Favourite, FavouriteAdmin)  


#Custom Admin class for the user's basket model
class BasketAdmin(admin.ModelAdmin):
    #Customize fields displayed in the admin list view
    list_display = ('id', 'user', 'waiter', 'session_id', 'created_at', 'updated_at')
    search_fields = ('user', 'waiter', 'session_id', 'created_at', 'updated_at')

#Register the Basket Model with the custom admin class
admin.site.register(Basket, BasketAdmin)


#Custom Admin class for the order items model
class OrderItemAdmin(admin.ModelAdmin):
    #Customize fields displayed in the admin list view
    list_display = ('basket', 'food_item', 'drink_item', 'price', 'soup_choice', 'spice_level', 'food_sauce', 'protein',
                    'has_ice', 'drink_size', 'desert_sauce', 'notes')
    search_fields = ('basket', 'food_item', 'drink_item', 'price')

#Register the Basket Model with the custom admin class
admin.site.register(OrderItem, OrderItemAdmin)


#Custom Admin class for the ratings model
class RatingAdmin(admin.ModelAdmin):
    #Customize fields displayed in the admin list view
    list_display = ('id', 'customer', 'customer_name', 'table', 'score', 'comments', 'submission_date')
    search_fields = ('customer', 'customer_name', 'table', 'score', 'comments', 'submission_date')
    
#Register the Ratings Model with the custom admin class
admin.site.register(Rating, RatingAdmin)

# Inline display of OrderItems
class OrderItemInline(admin.TabularInline):  # Or use StackedInline for a different layout
    model = OrderItem
    extra = 0  # Adjust to how many empty forms you want to display by default
    
    
#Custom Admin class for the order items model
class OrderAdmin(admin.ModelAdmin):
    #Customize fields displayed in the admin list view
    list_display = ('orderId', 'table', 'total_expected_duration', 'placed_at', 'basket', 'customer', 'customer_name', 'status', 'get_order_items', 'assigned_zone')
    search_fields = ('orderId', 'table', 'total_expected_duration', 'placed_at', 'basket', 'customer', 'customer_name', 'status', 'assigned_zone')

    # Custom method to display order items in the list view
    def get_order_items(self, obj):
        items = []
    
        for item in obj.order_items.all():
            if item.food_item:  # If there is a food_item
                items.append(str(item.food_item))
            elif item.drink_item:  # If there is a drink_item
                items.append(str(item.drink_item))
        
        return ", ".join(items)  # Join the items into a comma-separated string
    
    get_order_items.short_description = 'Order Items'
    
#Register the Order Model with the custom admin class
admin.site.register(Order, OrderAdmin)


#Custom Admin Class for the Kitchen Zone model
class KitchenZoneAdmin(admin.ModelAdmin):
    #Customize fields displayed in the admin list view
    list_display = ('zoneId', 'active_orders')
    search_fields = ('zoneId', 'active_orders')

#Register the Kitchen Model with the custom admin class
admin.site.register(KitchenZone, KitchenZoneAdmin)






