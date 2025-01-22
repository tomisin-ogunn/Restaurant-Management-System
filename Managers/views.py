from django.shortcuts import render, redirect
from django.http import HttpResponse
from Managers.models import Manager
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
@login_required
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

