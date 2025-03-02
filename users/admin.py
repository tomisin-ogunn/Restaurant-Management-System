from django.contrib import admin
from .models import Manager, Waiter, Customer

# Register your models here.

# Custom admin class for Manager
class ManagerAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('managerId', 'first_name', 'last_name', 'email', 'password')
    search_fields = ('managerId', 'first_name', 'last_name', 'email')

# Register the Manager model with the custom admin class
admin.site.register(Manager, ManagerAdmin)


#Custom admin class for Waiter
class WaiterAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('waiterId', 'first_name', 'last_name', 'email', 'password', 'first_login')
    search_fields = ('waiterId', 'first_name', 'last_name', 'email')
    
# Register the Waiter model (default registration)
admin.site.register(Waiter, WaiterAdmin)


#Custom admin class for Customer
class CustomerAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('customerId', 'first_name', 'last_name', 'email', 'password')
    search_fields = ('customerId', 'first_name', 'last_name', 'email')

# Register the Customer model (default registration)
admin.site.register(Customer, CustomerAdmin)


