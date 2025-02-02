from django.contrib import admin
from .models import Table

# Register your models here.

# Custom admin class for Table
class TableAdmin(admin.ModelAdmin):
    # Customize fields displayed in the admin list view
    list_display = ('tableNo', 'capacity', 'waiter', 'status')
    search_fields = ('tableNo', 'capacity', 'waiter', 'status')
    
# Register the Table model with the custom admin class
admin.site.register(Table, TableAdmin)