from django.contrib import admin
from .models import Table, Reservation, Food, Drink

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







