from django.contrib import admin
from .models import Customer

# Register your models here.

#Model Customer being registered
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customerId', 'first_name', 'last_name', 'email', 'password')
