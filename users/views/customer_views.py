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
from restaurant.models import Table, Reservation, Food, Drink
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.middleware.csrf import get_token
import string
import secrets
import re

# Create your views here.

#Function to display customer log in page
def displayCustomerLogin(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    get_token(request)
    
    return render(request, 'customers/login.html', context)    

#Function to authenticate customer login credentials
def customer_loginAuth(request):
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
            
            get_token(request)
            return redirect("customer-loggedIn-home")  # Redirect to home page

        except (Customer.DoesNotExist, ValueError):
            # Either the customer does not exist or the password is incorrect
            messages.error(request, "Invalid Email / Password")

            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
            }
            
            get_token(request)
            
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



