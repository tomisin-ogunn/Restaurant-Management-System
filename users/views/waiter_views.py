# Waiter Backend Views & Functipnalities for RMS JJ Web application

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
from restaurant.models import Table, Reservation, Food, Drink, Order, OrderItem, Basket
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import string
from django.middleware.csrf import get_token
import secrets
import re


# Create your views here.

#Function to display the waiter login page
def displayWaiterLogin(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    
    get_token(request)
    
    return render(request, 'waiters/login.html', context)    

#Function to authenticate waiter login credentials
def waiter_loginAuth(request):
    
    #Clear session
    request.session.flush()
    
    # Regenerate CSRF token after flushing the session
    get_token(request)
    
    if request.method == "POST":
        waiter_id = request.POST.get("waiter-username")  # Get waiterId from the form
        password = request.POST.get("waiter-password")  # Get password from the form
        
        try:
            # Fetch the waiter with the given waiterId
            waiter = Waiter.objects.get(waiterId=waiter_id)

            # Verify the password
            if not check_password(password, waiter.password):
                raise ValueError("Invalid credentials")  # Raise an error for incorrect password

            # Authentication successful, store waiter in session
            request.session["waiter_id"] = waiter.waiterId
            request.session["waiter_name"] = waiter.first_name
            
            # First login check
            if waiter.first_login is True:
                messages.success(request, "Change password!")  # Show first login message
                waiter.first_login = False  # Update first_login status
                waiter.save()
                context = {
                    "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
                    "waiterId": waiter_id
                }
                
                return render(request, "waiters/login.html", context)
            else:
                messages.success(request, "Login successful!")  # Normal login message
                
            return redirect("waiter-home")  # Redirect to home page
            

        except (Waiter.DoesNotExist, ValueError):
            # Either the manager does not exist or the password is incorrect
            messages.error(request, "Invalid Employee ID / Password")

            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
            }
            return render(request, "waiters/login.html", context)  # Render login form on failure

#Function to display Restaurant Waiter home interface after authentication
def displayWaiterHome(request):
    waiter_id = request.session.get("waiter_id")  # Get waiter_id from session
    
    #Retrieve the waiters notifications
    notifications = request.session.get(f"waiter_notifications_{waiter_id}", 0)
    
    if not request.session.session_key:
        request.session.create()  # Create a new session
    
    session_id = request.session.session_key
    
     #Get or create the basket using the session ID
    if waiter_id:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        basket, created = Basket.objects.get_or_create(waiter=waiter)
        
    else:
       basket, created = Basket.objects.get_or_create(session_id=session_id)
    
    #Retrieve the number of order items in basket
    order_items = OrderItem.objects.filter(basket=basket)
   
    order_item_count = order_items.count()
    
    food = Food.objects.all()
    drinks = Drink.objects.all()
    unique_categories = [choice[0] for choice in Food._meta.get_field('category').choices]
    drink_categories = [choice[0] for choice in Drink._meta.get_field('category').choices]
    
    if waiter_id:
        # Retrieve waiter details if authenticated
        try:
            waiter = Waiter.objects.get(waiterId=waiter_id)
            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
                "waiter": waiter,
                "food": food,
                "drinks": drinks,
                "categories": unique_categories,
                "drinkCategories": drink_categories,
                'order_item_count': order_item_count,
                'waiter_notifications': notifications
            }
            return render(request, "waiters/home.html", context)
        except Manager.DoesNotExist:
            # If manager not found in the database, clear the session and redirect to login
            messages.error(request, "Waiter not found. Please log in again.")
            return redirect("waiter-login")
    else:
        # If no session exists, redirect to login page
        messages.error(request, "You must be logged in to view this page.")
        return redirect("waiter-login")

#Function to update Waiters password
def updateWaiterPassword(request):
    if request.method == "POST":
        # Retrieve the passwords entered by the user
        new_password = request.POST.get("waiter-password")
        new_password2 = request.POST.get("waiter-password2")
        waiterID = request.POST.get("waiterId")
        
        try:
            # Find the manager by the provided email and update the password
            waiter = Waiter.objects.get(waiterId=waiterID)
            waiter.password = make_password(new_password)
            waiter.save()

            # Show success message
            messages.success(request, "Your password has been updated successfully!")

        except Waiter.DoesNotExist:
            messages.error(request, "Email does not exist.")
            
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, "waiters/login.html", context)

#Function to log waiter out
def waiterLogOut(request):
    # Clear the session
    request.session.flush()  # This clears all session data
    # Add a success message
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the login page
    
    get_token(request)
     
    return redirect("waiter-login")

#Function to verify if employee id exists in the waiters model
def waiterID_verifier(request):
    if request.method == "POST":
        waiterID = request.POST.get("waiter-id")
        if waiterID != "":
            try:
                # Check if email exists in the database
                waiter = Waiter.objects.get(waiterId=waiterID)
                messages.success(request, "ID exists!")
                context = {
                    'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
                    'waiterId': waiterID,  # Pass email to the template
                }
                return render(request, "waiters/login.html", context)  # Pass email to template
                
                
            except Waiter.DoesNotExist:
                    messages.error(request, "ID does not exist.")
                        
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, "waiters/login.html", context)

#Function to append an item to the waiter's basket
def addToBasketWaiter(request, itemID, itemType):
    waiter_id = request.session.get("waiter_id")  # Get  waiter_id from session
        
    #Obtain the session ID
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
        
    #Get or create the basket using the session ID
    if waiter_id:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        basket, created = Basket.objects.get_or_create(waiter=waiter)
        
    else:
       basket, created = Basket.objects.get_or_create(session_id=session_id)

    basket.save()
    
    if itemType == "mainMealFood":
        #Get the selected food or drink item
        food = get_object_or_404(Food, foodId=itemID)
        
        price = request.POST.get("foodPrice")
        soupChoice = request.POST.get("soupChoice")
        proteinChoice = request.POST.get("proteinChoice")
        spiceLevel = request.POST.get("spiceLevel")
        notes = request.POST.get("notes")
        
        if food.food_name == 'Pounded Yam' or food.food_name == 'Amala':
            order_item = OrderItem.objects.create(
                food_item=food,
                basket=basket,
                price=price,
                spice_level=spiceLevel,
                protein=proteinChoice,
                soup_choice=soupChoice,
                notes=notes
            )
            
        else:
            order_item = OrderItem.objects.create(
                food_item=food,
                basket=basket,
                price=price,
                spice_level=spiceLevel,
                protein=proteinChoice,
                notes=notes
            )
        
        order_item.save()
        
        messages.success(request, "Item added to basket!")
        context = {
            'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        }
        
        return render(request, "customers/home.html", context)
    
    elif itemType == "fastFood":
        #Get the selected food or drink item
        food = get_object_or_404(Food, foodId=itemID)
        
        price = request.POST.get("foodPrice2")
        sauce_choice = request.POST.get("sauceChoice")
        spiceLevel = request.POST.get("spiceLevel2")
        notes = request.POST.get("notes2")
        
        order_item = OrderItem.objects.create(
            food_item=food,
            basket=basket,
            price=price,
            food_sauce=sauce_choice,
            notes=notes,
            spice_level=spiceLevel
        )
        
        order_item.save()
        
        messages.success(request, "Item added to basket!")
        context = {
            'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        }
        
        return render(request, "customers/home.html", context)
    
    elif itemType == "deserts":
        #Get the selected food or drink item
        food = get_object_or_404(Food, foodId=itemID)
        
        price = request.POST.get("foodPrice3")
        sauce_choice = request.POST.get("sauceChoice3")
        notes = request.POST.get("notes3")
        
        order_item = OrderItem.objects.create(
            food_item=food,
            basket=basket,
            price=price,
            desert_sauce=sauce_choice,
            notes=notes
        )
        
        order_item.save()
        
        messages.success(request, "Item added to basket!")
        context = {
            'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        }
        
        return render(request, "customers/home.html", context)
    
    elif itemType == "drink":
        drink = get_object_or_404(Drink, drinkId=itemID)
        price = request.POST.get("drinkPrice")
        size = request.POST.get("drinkSize")
        notes = request.POST.get("drinkNotes")
        iceChoice = request.POST.get("iceChoice")
        
        order_item = OrderItem.objects.create(
            drink_item=drink,
            basket=basket,
            price=price,
            notes=notes,
            drink_size=size,
        )
        
        if iceChoice == "Ice":
            order_item.has_ice = True
        
        else:
            order_item.has_ice = False
                    
        order_item.save()
        
        messages.success(request, "Item added to basket!")
        context = {
            'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        }
        
        return render(request, "customers/home.html", context)

    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
        
    return render(request, "waiters/home.html", context)

#Function which displays the basket items for users to view
def displayBasketWaiter(request):
    # Get the session ID or waiter_id from the session
    waiter_id = request.session.get("waiter_id")
    session_id = request.session.session_key
    
    #Retrieve the waiters notifications
    notifications = request.session.get(f"waiter_notifications_{waiter_id}", 0)
    
    # Initialize basket based on session ID or waiter_id
    if  waiter_id:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        basket, created = Basket.objects.get_or_create(waiter=waiter)
    else:
        basket, created = Basket.objects.get_or_create(session_id=session_id)

    # Get the basket items (order items) for the basket
    order_items = OrderItem.objects.filter(basket=basket)
    order_item_count = order_items.count()
    
    # Calculate the total price, ensuring that prices are treated as floats
    total_price = sum(float(item.price.replace('£', '').strip()) for item in order_items)

    # Round the total to 2 decimal places
    total_price = round(total_price, 2)
    formatted_price = "{:.2f}".format(total_price)
    
    #Retrieve all the tables
    if waiter_id:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        tables = Table.objects.filter(waiter=waiter)
    else:
        tables = Table.objects.none() 
    
    # Prepare the context for the template
    context = {
        'basket': basket,
        'waiter': waiter,
        'order_items': order_items,
        'total_price': formatted_price,
        'order_item_count': order_item_count,
        'tables': tables,
        'media_url': settings.MEDIA_URL,  # Pass MEDIA_URL to the template
        'waiter_notifications': notifications
    }
    
    return render(request, "waiters/basket.html", context)

#Function to delete/remove basket item
def removeBasketItemWaiter(request, itemID):
    if request.method == "POST":
        basket_item = get_object_or_404(OrderItem, id=itemID)
        basket_item.delete()
    
    return JsonResponse({"success": True, "message": "Item removed from basket."})

#Function to delete all basket items
def deleteBasketItemsWaiter(request):
   # Get the session ID or customer email from the session
    waiter_id = request.session.get("waiter_id")  # Get  waiter_id from session
        
    #Obtain the session ID
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
        
    #Get or create the basket using the session ID
    if waiter_id:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        basket, created = Basket.objects.get_or_create(waiter=waiter)
        
    # Get the basket items (order items) for the basket
    order_items = OrderItem.objects.filter(basket=basket)

    # Delete all the order items in the basket
    order_items.delete()
    
    return JsonResponse({"success": True, "message": "Items removed from basket."})

#Function to fetch order item details
def fetchOrderItemDetailsWaiter(request, itemID):
    try:
        order_item = get_object_or_404(OrderItem, id=itemID)
        
        #Food Items
        if order_item.food_item:
            category = order_item.food_item.category 
            
            #Accounts for and toggles items that do not have a soup option
            if order_item.soup_choice:
                soupOption = order_item.soup_choice
            else:
                soupOption = "N/A"
                
                
            if order_item.notes:
                data = {
                    "success": True,
                    "spice": order_item.spice_level,
                    "soup": soupOption,
                    "food_sauce": order_item.food_sauce,
                    "protein": order_item.protein,
                    "desert_sauce": order_item.desert_sauce,
                    "notes": order_item.notes,
                    "itemType": "food",
                    "category": category
                }
            
            else:
               data = {
                    "success": True,
                    "spice": order_item.spice_level,
                    "soup": soupOption,
                    "food_sauce": order_item.food_sauce,
                    "protein": order_item.protein,
                    "desert_sauce": order_item.desert_sauce,
                    "notes": "N/A",
                    "itemType": "food",
                    "category": category
                }
        
        #Drink Items
        else:
            if order_item.notes:
                data = {
                    "success": True,
                    "size": order_item.drink_size,
                    "has_ice": order_item.has_ice,
                    "drink_notes": order_item.notes,
                    "itemType": "drink"
                }
            
            else:
                data = {
                    "success": True,
                    "size": order_item.drink_size,
                    "has_ice": order_item.has_ice,
                    "drink_notes": "N/A",
                    "itemType": "drink"
                }
                
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
        
#Function to generate order:
def generateOrderWaiter(request):
    # Get the session ID or customer email from the session
    waiter_id = request.session.get("waiter_id")  # Get  waiter_id from session
    session_id = request.session.session_key
    
    # Retrieve the basket based on session ID or customer email
    if waiter_id:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        basket, created = Basket.objects.get_or_create(waiter=waiter)
        
        tableNo = request.POST.get("order-table")
        name = request.POST.get("order-cus-name")
        
        table = Table.objects.get(tableNo=tableNo)
        
        # Get the basket items (order items) for the basket
        order_items = OrderItem.objects.filter(basket=basket)
        
        # Get the max duration from all the order items
        max_duration = max(
            int(order_item.food_item.duration.replace("mins", "").strip())  # Remove 'mins' and convert to integer
            for order_item in order_items if order_item.food_item is not None
        )
        
        order = Order(
            customer_name=name,
            table=table,
            basket=basket,
            total_expected_duration=max_duration
        )
        
        order.orderId = Order.generateOrderID()
        
        order.save()
        
        order.order_items.set(order_items) 
        
        # Clear the basket by disassociating the order items
        order_items.update(basket=None)
        
        # Increment the notification count for the waiter in the session
        notifications = request.session.get(f"waiter_notifications_{waiter_id}", 0) + 1
        request.session[f"waiter_notifications_{waiter_id}"] = notifications
        
        # Display success message and redirect
        messages.success(request, "Order created successfully!")
        
        context = {
            'media_url': settings.MEDIA_URL,  # Passing MEDIA_URL to template
            'order_id': order.orderId,
            'total_duration': max_duration 
        }
        return render(request, "waiters/basket.html", context)

    else:
        basket = Basket.objects.filter(session_id=session_id).first()
        tableNo = request.POST.get("order-table")
        name = request.POST.get("order-cus-name")
        
        table = Table.objects.get(tableNo=tableNo)
        
        # Get the basket items (order items) for the basket
        order_items = OrderItem.objects.filter(basket=basket)

        # # Get the max duration from all the order items
        max_duration = max(
            int(order_item.food_item.duration.replace("mins", "").strip())  # Remove 'mins' and convert to integer
            for order_item in order_items if order_item.food_item is not None 
        )
        
        order = Order(
            customer_name=name,
            table=table,
            basket=basket,
            total_expected_duration=max_duration
        )
    
        order.orderId = Order.generateOrderID()
        
        order.save()
        
        order.order_items.set(order_items)
        
        # Clear the basket by disassociating the order items
        order_items.update(basket=None)
        
        # Display success message and redirect
        messages.success(request, "Order created successfully!")
        
        context = {
            'media_url': settings.MEDIA_URL,  # Passing MEDIA_URL to template
            'order_id': order.orderId,
            'total_duration': max_duration 
        }
        return render(request, "waiters/basket.html", context)

#Function to display waiter notifications
def displayWaiterNotifications(request):
    waiter_id = request.session.get("waiter_id")
    notifications = request.session.get(f"waiter_notifications_{waiter_id}", 0)
    orders = []
    waiter = []
    
    # Reset the notification count after loading the page
    request.session[f"waiter_notifications_{waiter_id}"] = 0
    
    if not request.session.session_key:
        request.session.create()  # Create a new session
    
    session_id = request.session.session_key
    
     #Get or create the basket using the session ID
    if waiter_id:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        basket, created = Basket.objects.get_or_create(waiter=waiter)
        
        if waiter:
        # Fetch all tables assigned to this waiter
            tables = Table.objects.filter(waiter=waiter)
            
            # Get all orders linked to these tables
            orders = Order.objects.filter(table__in=tables).select_related("table")
        else:
            orders = []  # No orders if the waiter is not found
            waiter = None
        
    else:
       basket, created = Basket.objects.get_or_create(session_id=session_id)
    
    #Retrieve the number of order items in basket
    order_items = OrderItem.objects.filter(basket=basket)
   
    order_item_count = order_items.count()
    
    context = {
        "waiter_notifications": notifications,
        "waiter": waiter,
        'order_item_count': order_item_count,
        'waiter_notifications': notifications,
        "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template,
        'orders': orders
    }
    return render(request, "waiters/notifications.html", context)











