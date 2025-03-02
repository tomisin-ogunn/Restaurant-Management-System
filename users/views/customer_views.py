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
import string
import secrets
import re

# Create your views here.

#Function to display customer log in page
def displayCustomerLogin(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
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
            return redirect("customer-home")  # Redirect to home page

        except (Customer.DoesNotExist, ValueError):
            # Either the customer does not exist or the password is incorrect
            messages.error(request, "Invalid Email / Password")

            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
            }
            return render(request, "customers/login.html", context)  # Render login form on failure

#Function to display Customer home interface after authentication
def displayCustomerHome(request):
    customer_email = request.session.get("customer_email")  # Get customer_email from session
    if customer_email:
        # Retrieve customer details if authenticated
        try:
            customer = Customer.objects.get(email=customer_email)
            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
                "customer": customer,
            }
            return render(request, "customers/home.html", context)
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












