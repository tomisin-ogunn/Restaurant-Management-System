# Kitchen Backend Views & Functipnalities for RMS JJ Web application

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.utils import timezone
from users.models import Manager, Waiter
from restaurant.models import Table, Reservation, Food, Drink, Order, OrderItem, Basket, KitchenZone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import string
from django.middleware.csrf import get_token
import secrets
import re

# Create your views here.

#Function to display the cooking zones
def displayKitchenZone(request, zoneID):
    # Fetch the specific kitchen zone by its ID, or 404 if it doesn't exist
    zone = get_object_or_404(KitchenZone, zoneId=zoneID)
    
    context = {
            "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
            'zone': zone,
        }
    # Pass the kitchen zone and its orders to the template
    return render(request, 'kitchen_zone_detail.html', context)







