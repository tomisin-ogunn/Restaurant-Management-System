from django.contrib import admin
from .models import Table, Reservation

# Register your models here.

#Model Table being registered
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('tableNo', 'capacity', 'waiterId', 'status')
    
#Model Reservation being registered    
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservationId', 'customer_name', 'time_booked', 'tableNo', 'comments', 'duration', 'size', 'customerId')
    list_filter = ('time_booked',)
    search_fields = ('customer_name',)