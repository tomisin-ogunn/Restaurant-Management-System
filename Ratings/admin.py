from django.contrib import admin
from .models import Rating

# Register your models here.

#Model Rating being registered
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ratingID', 'tableNo', 'score', 'comments', 'submission_date', 'customer')