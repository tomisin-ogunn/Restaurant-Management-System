from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from .models import Manager, Waiter
import string
import secrets
import re


# Create your views here.

#Function to display login page for managers
def display_managerLogin(request):
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, 'managers/login.html', context)

#Function to authenticate manager login credentials
def manager_loginAuth(request):
    if request.method == "POST":
        manager_id = request.POST.get("username")  # Get managerId from the form
        password = request.POST.get("password")  # Get password from the form

        try:
            # Fetch the manager with the given managerId
            manager = Manager.objects.get(managerId=manager_id)

            # Verify the password
            if check_password(password, manager.password):
                # Authentication successful, store manager in session
                request.session["manager_id"] = manager.managerId
                request.session["manager_name"] = manager.first_name
                messages.success(request, "Login successful!")
                return redirect("manager-home")  # Redirect to home page
            else:
                # Incorrect password
                messages.error(request, "Invalid Employee ID / Password")
        except Manager.DoesNotExist:
            # Manager with the given managerId does not exist
            messages.error(request, "Manager ID not found. Please try again.")

    context = {
        "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
    }
    return render(request, "managers/login.html", context)  # Render login form on failure

#Function to display Restaurant Manager home interface after authentication
def displayManagerHome(request):
    manager_id = request.session.get("manager_id")  # Get manager_id from session
    if manager_id:
        # Retrieve manager details if authenticated
        try:
            manager = Manager.objects.get(managerId=manager_id)
            context = {
                "media_url": settings.MEDIA_URL,  # Passing MEDIA_URL to the template
                "manager": manager,
            }
            return render(request, "managers/home.html", context)
        except Manager.DoesNotExist:
            # If manager not found in the database, clear the session and redirect to login
            messages.error(request, "Manager not found. Please log in again.")
            return redirect("manager-login")
    else:
        # If no session exists, redirect to login page
        messages.error(request, "You must be logged in to view this page.")
        return redirect("manager-login")

#Function to log out the manager
def manager_logout(request):
    # Clear the session
    request.session.flush()  # This clears all session data
    # Add a success message
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the login page
    return redirect("manager-login")

#Function to verify if email address exists in the managers model
def managerEmail_verifier(request):
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
                return render(request, "managers/login.html", context)  # Pass email to template
                
                
            except Manager.DoesNotExist:
                    messages.error(request, "Email does not exist.")
                        
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    return render(request, "managers/login.html", context)

#Function to update Managers password
def update_ManagerPassword(request):
    if request.method == "POST":
        # Retrieve the passwords entered by the user
        new_password = request.POST.get("manpassword")
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
    return render(request, "managers/login.html", context)

#Function to display waiter management interface
def displayWaiterManagement(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
     
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        "manager": manager,
    }
    return render(request, 'managers/waiter_management.html', context)

#Function to display add waiter form
def displayWaiterAddForm(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
     
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        "manager": manager,
    }
    return render(request, 'managers/add_waiter.html', context)


#Function to generate a random password
def generate_random_password(length=8):
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

#Function to append waiter into database
def addWaiter(request):
       # Retrieve the form data from the POST request
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("waiter-email")

        try:
            
            #Generate random password
            generated_password = generate_random_password()
            
            # Create the new waiter entry
            new_waiter = Waiter(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(generated_password)  # Hash the password for security
            )
            
            # Generate the Waiter ID (JJW0001 format)
            new_waiter.waiterId = Waiter.generateWaiterID()

            # Save the new waiter to the database
            new_waiter.save()

            # Display success message
            messages.success(request, "Waiter added successfully!")
            context = {
                'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
                'generated_password': generated_password
            }
            return render(request, "managers/add_waiter.html", context)


        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        context = {
            'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        }
        return render(request, "managers/add_waiter.html", context)




















