from django.contrib import admin
from .models import Table, Reservation

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
    list_display = ('reservationId', 'size', 'comments', 'tableNo', 'duration', 'time_booked', 'customer_name', 'reservation_date')
    search_fields = ('reservationId', 'size', 'comments', 'tableNo', 'duration', 'time_booked', 'customer_name', 'reservation_date')
    
#Register the Reservation model with the custom admin class
admin.site.register(Reservation, ReservationAdmin)


