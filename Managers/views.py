from django.shortcuts import render
from django.http import HttpResponse
from Managers.models import Manager

# Create your views here.

#Function to display Restaurant Manager login page

def display_managerlogin(request):
    return render(request, 'manager/login.html')

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