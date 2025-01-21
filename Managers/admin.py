from django.contrib import admin
from .models import Manager

# Register your models here.

#Model Manager being registered    
class ManagerAdmin(admin.ModelAdmin):
    # You can customize which fields to display in the admin
    list_display = ('managerId', 'first_name', 'last_name', 'email', 'password')
    search_fields = ('managerId', 'first_name', 'last_name', 'email')


admin.site.register(Manager, ManagerAdmin)