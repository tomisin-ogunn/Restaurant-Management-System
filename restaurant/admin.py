from django.contrib import admin
from .models import Table, Reservation, Food, Drink, Favourite, Basket, OrderItem

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
    list_display = ('id', 'user', 'session_id', 'created_at', 'updated_at')
    search_fields = ('user', 'session_id', 'created_at', 'updated_at')

#Register the Basket Model with the custom admin class
admin.site.register(Basket, BasketAdmin)


#Custom Admin class for the order items model
class OrderItemAdmin(admin.ModelAdmin):
    #Customize fields displayed in the admin list view
    list_display = ('basket', 'food_item', 'drink_item', 'price', 'spice_level', 'food_sauce', 'protein',
                    'has_ice', 'drink_size', 'desert_sauce', 'notes')
    search_fields = ('basket', 'food_item', 'drink_item', 'price')
#Register the Basket Model with the custom admin class
admin.site.register(OrderItem, OrderItemAdmin)





