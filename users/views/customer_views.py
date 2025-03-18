# Customer Backend Views & Functipnalities for RMS JJ Web application

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.utils import timezone
from users.models import Manager, Waiter, Customer
from restaurant.models import Table, Reservation, Food, Drink, Favourite, Basket, OrderItem, Rating, Order
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.middleware.csrf import get_token
import string
import secrets
import re

# Create your views here.

#Function to display Customer home interface
def displayCustomerHome(request):
    customer_email = request.session.get("customer_email")  # Get customer_email from session
    if not request.session.session_key:
        request.session.create()  # Create a new session
    
    session_id = request.session.session_key

    food = Food.objects.all()
    drinks = Drink.objects.all()
    unique_categories = [choice[0] for choice in Food._meta.get_field('category').choices]
    drink_categories = [choice[0] for choice in Drink._meta.get_field('category').choices]
    
    #Get or create the basket using the session ID
    if customer_email:
        customer = Customer.objects.get(email=customer_email)
        basket, created = Basket.objects.get_or_create(user=customer)
        
    else:
       basket, created = Basket.objects.get_or_create(session_id=session_id)


    order_items = OrderItem.objects.filter(basket=basket)
   
    order_item_count = order_items.count()
    
    context = {
        "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
        "food": food,
        "drinks": drinks,
        "categories": unique_categories,
        "drinkCategories": drink_categories,
        'order_item_count': order_item_count
    }
    return render(request, "customers/home.html", context)

#Function to regenerate a user session
def regenerate_session(request):
    request.session.flush()  # Clears the current session data and starts a new one
    request.session.create()
    return JsonResponse({"status": "Session regenerated"})

#Function to display customer log in page
def displayCustomerLogin(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    get_token(request)
    
    return render(request, 'customers/login.html', context)    

#Function to authenticate customer login credentials
def customer_loginAuth(request):
    #Clear session
    request.session.flush()
    
    # Regenerate CSRF token after flushing the session
    get_token(request)
    
    if request.method == "POST":
        email = request.POST.get("customer-email", "").strip()  # Get email from the form
        password = request.POST.get("customer-password")  # Get password from the form
        
        try:
            # Fetch the customer with the given customer email
            customer = Customer.objects.get(email=email)

            # Verify the password
            if not check_password(password, customer.password):
                raise ValueError("Invalid credentials")  # Raise an error for incorrect password

            # Authentication successful, store customer in session
            request.session["customer_email"] = customer.email
            request.session["customer_name"] = customer.first_name
            messages.success(request, "Login successful!")
            
            return redirect("customer-loggedIn-home")  # Redirect to home page

        except (Customer.DoesNotExist, ValueError):
            # Either the customer does not exist or the password is incorrect
            messages.error(request, "Invalid Email / Password")

            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
            }
            
            return render(request, "customers/login.html", context)  # Render login form on failure

#Function to display Customer home interface after authentication
def displayCustomerLoggedInHome(request):
    customer_email = request.session.get("customer_email")  # Get customer_email from session
    food = Food.objects.all()
    drinks = Drink.objects.all()
    unique_categories = [choice[0] for choice in Food._meta.get_field('category').choices]
    drink_categories = [choice[0] for choice in Drink._meta.get_field('category').choices]
     
    if customer_email:
        # Retrieve customer details if authenticated
        try:
            customer = Customer.objects.get(email=customer_email)
            
            # Retrieve favourites for the customer
            favourites = Favourite.objects.filter(customer_id=customer).select_related("food_id", "drink_id")
            food_favourites = [fav.food_id.foodId for fav in favourites if fav.food_id]
            drink_favourites = [fav.drink_id.drinkId for fav in favourites if fav.drink_id]
            
            for item in food:
                item.fav_status = "favourited" if item.foodId in food_favourites else "unfavourited"

            for item in drinks:
                item.fav_status = "favourited" if item.drinkId in drink_favourites else "unfavourited"
            
            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
                "customer": customer,
                "food": food,
                "drinks": drinks,
                "categories": unique_categories,
                "drinkCategories": drink_categories
            }
            return render(request, "customers/logged_in_home.html", context)
        except Customer.DoesNotExist:
            # If customer not found in the database, clear the session and redirect to login
            messages.error(request, "Customer not found. Please log in again.")
            return redirect("customer-login")
    else:
        # If no session exists, redirect to login page
        messages.error(request, "You must be logged in to view this page.")
        return redirect("customer-login")

#Function to verify if email address exists in the customers model
def customerEmail_verifier(request):
    if request.method == "POST":
        email = request.POST.get("customerEmail", "").strip()
        if email != "":
            try:
                # Check if email exists in the database
                customer = Customer.objects.get(email=email)
                messages.success(request, "Email exists!")
                context = {
                    'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
                    'email': email,  # Pass email to the template
                }
                return render(request, "customers/login.html", context)  # Pass email to template
                
                
            except Customer.DoesNotExist:
                    messages.error(request, "Email does not exist.")
                        
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, "customers/login.html", context)

#Function to update Managers password
def update_CustomerPassword(request):
    if request.method == "POST":
        # Retrieve the passwords entered by the user
        new_password = request.POST.get("customer-password")
        email = request.POST.get("customer-email-add")
        
        try:
            # Find the customer by the provided email and update the password
            customer = Customer.objects.get(email=email)
            customer.password = make_password(new_password)
            customer.save()

            # Show success message
            messages.success(request, "Your password has been updated successfully!")

        except Customer.DoesNotExist:
            messages.error(request, "Email does not exist.")
            
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, "customers/login.html", context)

#Function which displays the customer Register Form
def displayCustomerRegister(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, 'customers/register.html', context)    

#Function which appends a customer to the Django Model after registration
def appendCustomer(request):
    if request.method == "POST":
        #Retrieve form inputs
        first_name = request.POST.get("customer-FirstName")
        last_name = request.POST.get("customer-LastName")
        email = request.POST.get("customer-Email")
        password = request.POST.get("customer-Password")
        
        try:
            #Create new customer
            new_customer = Customer(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = make_password(password)
            )
            
            #Generate customer Id
            new_customer.customerId = Customer.generateCustomerID()
            
            #Save the new customer to the Django Model
            new_customer.save()
            
            # Display success message
            messages.success(request, "Registration Completed!")
            context = {
                'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
            }
            
            return render(request, "customers/register.html", context)

            
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    
    return render(request, "customers/register.html", context)

#Function to log customer out
def customerLogOut(request):
    # Clear the session
    request.session.flush()  # This clears all session data
    # Add a success message
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the login page
    
    get_token(request)
     
    return redirect("customer-login")

#Function which appends an item to customers favourites
@csrf_exempt 
def addItemToFavourites(request, itemID, itemType):
    if request.method == "POST":
        customer_id = request.POST.get("customerId")
        customer = get_object_or_404(Customer, customerId=customer_id)
        
        
        if itemType == "food":
            food = get_object_or_404(Food, foodId=itemID)
            #Create the favourited item
            favourited_item = Favourite(
                customer_id = customer,
                food_id = food
            )
            
        elif itemType == "drink":
            drink = get_object_or_404(Drink, drinkId=itemID)
            #Create the favourited item
            favourited_item = Favourite(
                customer_id = customer,
                drink_id = drink
            )
            
        if favourited_item:
            favourited_item.save()
            return JsonResponse({"message": "Item added to favourites successfully!"})
            
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

#Function which returns/dislays the customer favourites page
def displayCustomerFavourites(request):
    customer_email = request.session.get("customer_email")  # Get customer_email from session
    
    if customer_email:
        customer = Customer.objects.get(email=customer_email)
       
        #Fetch the favourites for the customer
        favourites = Favourite.objects.filter(customer_id=customer).select_related("food_id", "drink_id")

        # Separate food and drink objects
        food_favourites = [fav.food_id for fav in favourites if fav.food_id]
        drink_favourites = [fav.drink_id for fav in favourites if fav.drink_id]
        unique_categories = [choice[0] for choice in Food._meta.get_field('category').choices]
        drink_categories = [choice[0] for choice in Drink._meta.get_field('category').choices]
    
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        'customer': customer,
        'food': food_favourites,
        'drinks': drink_favourites,
        "categories": unique_categories,
        "drinkCategories": drink_categories
    }
    return render(request, 'customers/favourites.html', context) 

#Function which removes an item from customers favourites
@csrf_exempt
def removeItemFromFavourites(request, itemID, itemType):
    if request.method == "POST":
        customer_id = request.POST.get("customerId")
        customer = get_object_or_404(Customer, customerId=customer_id)
        
        
        if itemType == "food":
            food = get_object_or_404(Food, foodId=itemID)
            
            # Get the favourited item and delete it
            favourite = get_object_or_404(Favourite, customer_id=customer, food_id=food)
            favourite.delete()

        elif itemType == "drink":
            drink = get_object_or_404(Drink, drinkId=itemID)
            
            # Get the favourited item and delete it
            favourite = get_object_or_404(Favourite, customer_id=customer, drink_id=drink)
            favourite.delete()
        return JsonResponse({"message": "Item removed from favourites successfully!"})

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

#Function to add menu item to the basket
@login_required
def addToBasket(request, itemID, itemType):
    customer_email = request.session.get("customer_email")  # Get customer_email from session
        
    #if request.method == "POST":
    #Obtain the session ID
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
        
    #Get or create the basket using the session ID
    if customer_email:
        customer = Customer.objects.get(email=customer_email)
        basket, created = Basket.objects.get_or_create(user=customer)
        
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
        
    return render(request, "customers/home.html", context)

#Function which displays the basket items for users to view
def displayBasket(request):
    # Get the session ID or customer email from the session
    customer_email = request.session.get("customer_email")
    session_id = request.session.session_key
    
    # Initialize basket based on session ID or customer email
    if customer_email:
        customer = get_object_or_404(Customer, email=customer_email)
        basket, created = Basket.objects.get_or_create(user=customer)
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
    tables = Table.objects.all()
    
    # Prepare the context for the template
    context = {
        'basket': basket,
        'order_items': order_items,
        'total_price': formatted_price,
        'order_item_count': order_item_count,
        'tables': tables,
        'media_url': settings.MEDIA_URL,  # Pass MEDIA_URL to the template
    }
    
    return render(request, "customers/basket.html", context)

#Function to delete/remove basket item
def removeBasketItem(request, itemID):
    if request.method == "POST":
        basket_item = get_object_or_404(OrderItem, id=itemID)
        basket_item.delete()
    
    return JsonResponse({"success": True, "message": "Item removed from basket."})

#Function which displays customer rating/feedback form
def displayCustomerRatingForm(request):
    session_id = request.session.session_key

    basket = Basket.objects.get(session_id=session_id)
    order_items = OrderItem.objects.filter(basket=basket)
    order_item_count = order_items.count()
    tables = Table.objects.all()
    
    context = {
        "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
        'order_item_count': order_item_count,
        'tables': tables
    }
    return render(request, "customers/rating.html", context)
    
#Function which creates a customer rating
@login_required
def createCustomerRating(request):
    customer_email = request.session.get("customer_email")  # Get customer_email from session
    
    if request.method == "POST":
        name = request.POST.get("cus-name")
        score = request.POST.get("rating-score")
        comments = request.POST.get("cus-comments")
        tableNo = request.POST.get("cus-tables")
        table = Table.objects.get(tableNo=tableNo)
        
        if customer_email:
            customer = Customer.objects.get(email=customer_email)
            rating = Rating(
                customer=customer,
                customer_name=name,
                score=score,
                comments=comments,
                table=table
            )
                
        else:
            rating = Rating(
                customer_name=name,
                score=score,
                comments=comments,
                table=table
            )
            
    if rating:
        rating.save()
    
    messages.success(request, "Feedback sent!")
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    
    return render(request, "customers/rating.html", context)
        
#Function to delete all basket items
def deleteBasketItems(request):
   # Get the session ID or customer email from the session
    customer_email = request.session.get("customer_email")
    session_id = request.session.session_key

    # Initialize basket based on session ID or customer email
    if customer_email:
        customer = Customer.objects.get(email=customer_email)
        basket, created = Basket.objects.get_or_create(user=customer)
        
    else:
       basket, created = Basket.objects.get_or_create(session_id=session_id)


    # Get the basket items (order items) for the basket
    order_items = OrderItem.objects.filter(basket=basket)

    # Delete all the order items in the basket
    order_items.delete()
    
    return JsonResponse({"success": True, "message": "Items removed from basket."})

#Function to fetch order item details
def fetchOrderItemDetails(request, itemID):
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
def generateOrder(request):
    # Get the session ID or customer email from the session
    customer_email = request.session.get("customer_email")
    session_id = request.session.session_key
    
    # Retrieve the basket based on session ID or customer email
    if customer_email:
        customer = get_object_or_404(Customer, email=customer_email)
        basket, created = Basket.objects.get_or_create(user=customer)
        
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
            customer=customer,
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
        return render(request, "customers/basket.html", context)

    else:
        basket, created = Basket.objects.get_or_create(session_id=session_id)
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
        return render(request, "customers/basket.html", context)



