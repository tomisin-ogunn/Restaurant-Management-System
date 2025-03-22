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
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
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
    orders = Order.objects.filter(assigned_zone=zone, status="Assigned")
    
    #Count the number of active orders
    active_orders =  orders.count()
    
    # Calculate the total price for each order
    for order in orders:
        total_price = sum(float(item.price.replace('£', '').strip()) for item in order.order_items.all())
        order.total_price = round(total_price, 2)
        
    context = {
            "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
            'zone': zone,
            "orders": orders,
            'active_orders': active_orders
        }
    # Pass the kitchen zone and its orders to the template
    return render(request, 'kitchen_zone_detail.html', context)

# Dynamic Load Balancing Scheduling logic
def assign_order_to_zone(order):
    zones = list(KitchenZone.objects.all().order_by('zoneId'))  # Get zones in order
    total_orders = Order.objects.filter(status='Assigned').count() # Count active orders
    
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

#Function which dynamically updates orders for kitchen zones in real time
def get_kitchen_orders(request, zoneID):
    zone = get_object_or_404(KitchenZone, zoneId=zoneID)
    orders = Order.objects.filter(assigned_zone=zone)

    # Prepare the orders data for JSON response
    orders_data = []
    for order in orders:
        total_price = sum(float(item.price.replace('£', '').strip()) for item in order.order_items.all())
        order.total_price = round(total_price, 2)

        order_data = {
            "orderId": order.orderId,
            "customer_name": order.customer_name,
            "table": order.table.tableNo,
            "status": order.status,
            "total_expected_duration": order.total_expected_duration,
            "total_price": order.total_price,
            "placed_at": order.placed_at,
            "order_items": []
        }

        for item in order.order_items.all():
            item_data = {
               "food_name": item.food_item.food_name if item.food_item else None,
                "drink_name": item.drink_item.drink_name if item.drink_item else None,
                "price": item.price,
                "spice_level": item.spice_level,
                "protein": item.protein,
                "food_sauce": item.food_sauce,
                "soup_choice": item.soup_choice,
                "desert_sauce": item.desert_sauce,
                "notes": item.notes,
                "drink_size": item.drink_size,
                "has_ice": item.has_ice
            }
            order_data["order_items"].append(item_data)

        orders_data.append(order_data)

    return JsonResponse({"orders": orders_data})
    



