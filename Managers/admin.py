from django.contrib import admin
from .models import Manager

# Register your models here.

#Model Manager being registered
@admin.register(Manager)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('managerId', 'first_name', 'last_name', 'password', 'email')
    search_fields = ('managerId',)