# Kitchen Backend Views & Functionalities for RMS JJ Web application

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
    
    #Retrieve the assigned orders  
    orders = Order.objects.filter(assigned_zone=zone)
    
    # Calculate the total price for each order
    for order in orders:
        total_price = sum(float(item.price.replace('£', '').strip()) for item in order.order_items.all())
        order.total_price = round(total_price, 2)
        
    context = {
            "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
            'zone': zone,
            "orders": orders
        }
    # Pass the kitchen zone and its orders to the template
    return render(request, 'kitchen_zone_detail.html', context)

# Dynamic Load Balancing Scheduling logic
def assign_order_to_zone(order):
    zones = list(KitchenZone.objects.all().order_by('zoneId'))  # Get zones in order
    total_orders = Order.objects.filter(status='Assigned').count() # Count active & pending orders
    
    # Determine the next zone in sequence (1 → 2 → 3 → Repeat)
    next_zone_index = total_orders % len(zones)  # Cycles through index 0, 1, 2 (Zone 1, 2, 3)

    # Get the next zone in round-robin sequence
    selected_zone = zones[next_zone_index]

    if selected_zone.active_orders < 3:
        # Assign order to this zone
        order.assigned_zone = selected_zone
        order.status = 'Assigned'
        selected_zone.active_orders += 1
        #selected_zone.total_remaining_time += order.total_expected_duration
        selected_zone.save()
    # else:
    #     # If all zones are full, find the least busy one for pending queue
    #     least_busy_zone = min(zones, key=lambda z: (z.active_orders, z.total_remaining_time))
    #     order.assigned_zone = least_busy_zone
    #     order.status = 'pending'  # Mark as waiting

    order.save()





