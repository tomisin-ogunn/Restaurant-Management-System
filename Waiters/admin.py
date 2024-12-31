from django.contrib import admin
from .models import Waiter

# Register your models here.

#Model Waiter being registered
@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
    list_display = ('waiterId', 'first_name', 'last_name', 'email', 'password')




