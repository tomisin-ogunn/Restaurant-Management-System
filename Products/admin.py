from django.contrib import admin
from .models import Food, Drink

# Register your models here.

#Model Food being registered
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'ingredients', 'duration', 'allergen', 'image')
    search_fields = ('name',)
    
#Model Drink being registered
@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'description', 'alcoholConc', 'image')
    search_fields = ('name',)