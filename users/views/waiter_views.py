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
from restaurant.models import Table, Reservation, Food, Drink
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import string
import secrets
import re


# Create your views here.

#Function to display the waiter login page
def displayWaiterLogin(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, 'waiters/login.html', context)    

#Function to authenticate waiter login credentials
def waiter_loginAuth(request):
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
    waiter_id = request.session.get("waiter_id")  # Get manager_id from session
    if waiter_id:
        # Retrieve manager details if authenticated
        try:
            waiter = Waiter.objects.get(waiterId=waiter_id)
            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
                "waiter": waiter,
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





