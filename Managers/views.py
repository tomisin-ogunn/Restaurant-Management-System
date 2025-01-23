from django.shortcuts import render, redirect
from django.http import HttpResponse
from Managers.models import Manager
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import re


# Create your views here.

#Function to display Restaurant Manager login page
def display_managerlogin(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, 'manager/login.html', context)

def create_manager(request):
    # Attempting to get the first manager instance
    manager_instance = Manager.objects.first()

    # If no managers exist, manager_instance will be None
    if manager_instance is None:
        # If there is no manager in the database, generate a new ID
        new_manager_id = Manager.generateManagerID()  # Generate the ID using the class method
    else:
        # If a manager instance exists, use it
        new_manager_id = manager_instance.generateManagerID()  # Use the instance method

    # Now you can create a new manager using the generated ID
    new_manager = Manager.objects.create(
        managerId=new_manager_id,  # Generated ID
        first_name="John",          # First name
        last_name="Doe",            # Last name
        password="securepassword",  # Password (hashed in real-world scenarios)
        email="john.doe@example.com"  # Email
    )

    # Return a response with the new manager ID
    return HttpResponse(f"New manager created with ID: {new_manager.managerId}")

#Function to display Restaurant Manager home interface
@login_required(login_url="manager_login")
def displayHomePage(request):
    context = {
        'media_url': settings.MEDIA_URL,
        'user': request.user,
    }
    return render(request, 'manager/home.html', context)

#Function to perform authentication process of manager during login
def manager_login(request):
    if request.method == "POST":
        employeeID = request.POST.get("username")
        password = request.POST.get("password")
        
        #Authenticate the user
        user = authenticate(request, managerId=employeeID, password=password)
        print(f"Authenticated User: {user}")

        if user is not None:
            #Login the user
            login(request, user)
            #redirect the user to the home page
            print(f"This worked!!")
            return redirect("home")
            
        else:
            messages.error(request, "Invalid Employee ID / Password")
            print(f"ERROR!!")
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
     
    return render(request, "manager/login.html", context)

#Function to verify if email address exists in the managers model
def email_verifier(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if email != "":
            try:
                # Check if email exists in the database
                manager = Manager.objects.get(email=email)
                messages.success(request, "Email exists!")
                context = {
                    'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
                    'email': email,  # Pass email to the template
                }
                return render(request, "manager/login.html", context)  # Pass email to template
                
                
            except Manager.DoesNotExist:
                    messages.error(request, "Email does not exist.")
                        
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, "manager/login.html", context)

#Function to update password
def update_password(request):
    if request.method == "POST":
        # Retrieve the passwords entered by the user
        new_password = request.POST.get("manpassword")
        confirm_password = request.POST.get("manpassword2")
        email = request.POST.get("hiddenEmail")
        
        try:
            # Find the manager by the provided email and update the password
            manager = Manager.objects.get(email=email)
            manager.password = make_password(new_password)
            manager.save()

            # Show success message and redirect to login page
            messages.success(request, "Your password has been updated successfully!")
            # return redirect("manager_login")  # Redirect back to login page

        except Manager.DoesNotExist:
            messages.error(request, "Email does not exist.")
            
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, "manager/login.html", context)