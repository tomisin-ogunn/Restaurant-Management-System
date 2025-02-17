from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from .models import Manager, Waiter
from restaurant.models import Table, Reservation, Food, Drink
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
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
            if not check_password(password, manager.password):
                raise ValueError("Invalid credentials")  # Raise an error for incorrect password

            # Authentication successful, store manager in session
            request.session["manager_id"] = manager.managerId
            request.session["manager_name"] = manager.first_name
            messages.success(request, "Login successful!")
            return redirect("manager-home")  # Redirect to home page

        except (Manager.DoesNotExist, ValueError):
            # Either the manager does not exist or the password is incorrect
            messages.error(request, "Invalid Employee ID / Password")

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

            # Show success message
            messages.success(request, "Your password has been updated successfully!")

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

#Function to display edit waiter form
def displayWaiterEditForm(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
    waiters = Waiter.objects.all()
     
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        "manager": manager,
        'waiters': waiters
    }
    return render(request, 'managers/edit_waiter.html', context)
    
#Function to fetch waiter details
def get_waiter_details(request, waiter_id):
    try:
        waiter = Waiter.objects.get(waiterId=waiter_id)
        data = {
            "success": True,
            "first-name": waiter.first_name,
            "last-name": waiter.last_name,
            "email": waiter.email,
        }
        return JsonResponse(data)
    except Waiter.DoesNotExist:
        return JsonResponse({"success": False, "message": "Waiter not found"}, status=404)
    
#Function to update waiter details
def updateWaiterDetails(request):
    if request.method == "POST":
        #Retrieve form inputs
        upd_first_name = request.POST.get("updfirst-name")
        upd_last_name = request.POST.get("updlast-name")
        upd_email = request.POST.get("waiter-email")
        waiter_id = request.POST.get("updWaiterID")

        #Get the specific waiter being edited
        try:
            waiter = Waiter.objects.get(waiterId=waiter_id)
            waiter.first_name = upd_first_name
            waiter.last_name = upd_last_name
            waiter.email = upd_email
            waiter.save()
            
            # Show success message
            messages.success(request, "Waiter details have been successfully updated!")

        except Waiter.DoesNotExist:
            messages.error(request, "Waiter does not exist.")
        
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    
    return render(request, "managers/edit_waiter.html", context)

#Function to display assign waiter form
def displayAssignWaiterForm(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
    waiters = Waiter.objects.all()
    tables = Table.objects.all()
     
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        "manager": manager,
        'waiters': waiters,
        'tables': tables
    }

    return render(request, 'managers/assign_waiter.html', context)
    
#Function to assign waiter (mapping each waiter to table)
def assignWaiter(request):
    if request.method == "POST":
        #Retrieve form inputs
        waiter_id = request.POST.get("waiters", "")[:7]
        tableNo = request.POST.get("tables")
        
        #Assign waiter to table
        try:
            table = Table.objects.get(tableNo=tableNo)
            waiter = get_object_or_404(Waiter, waiterId=waiter_id)
            table.waiter = waiter
            table.save()
            
            # Show success message
            messages.success(request, "Waiter has been successfully assigned!")
            
        except Waiter.DoesNotExist:
            messages.error(request, "Waiter does not exist.")
            
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
    }
    
    return render(request, "managers/assign_waiter.html", context)

#Function which displays table reservation interface for managers
def displayTableReservation(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
    tables = Table.objects.all()

    reservations = Reservation.objects.all()
    
    for reservation in reservations:
        if reservation.time_elapsed:
            # Update table status if it's still marked as reserved
           continue
        else:
            pass
        
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        'tables': tables,
        'manager': manager
    }
    return render(request, 'managers/reserve_table.html', context)

#Function to fetch table details from model
def get_table_details(request, tableId):    
    try:
        table = Table.objects.select_related('waiter').get(tableNo=tableId)
        data = {
            "success": True,
            "capacity": table.capacity,
            "status": table.status,
            "waiter": {
                "id": table.waiter.waiterId if table.waiter else None,
                "name": f"{table.waiter.first_name} {table.waiter.last_name}" if table.waiter else None
            },
        }
        return JsonResponse(data)
    except Table.DoesNotExist:
        return JsonResponse({"success": False, "message": "Table not found"}, status=404)
        
#Function to create a reservation (append to the model)
def generateReservation(request):
    if request.method == "POST":
        # Retrieve form inputs
        table_No = request.POST.get("tableNo")
        date = request.POST.get("reservationDate")
        start_time = request.POST.get("reservationStartTime")
        end_time = request.POST.get("reservationEndTime")
        duration = request.POST.get("reservationDuration")
        size = int(request.POST.get("reservationSize", 0))
        comments = request.POST.get("reservationComments")
        customer_name = request.POST.get("customer-name")
        capacity = int(request.POST.get("tableCapacity", 0))

        # Verify that size is not greater than capacity
        if size > capacity:
            messages.error(request, "Size is bigger than table capacity!")
            return redirect("reservation_page")  # Redirect to the reservation form page

        try:
            # Fetch the table instance
            table = get_object_or_404(Table, tableNo=table_No)
            table.status = "reserved"
            table.save()

            # Create reservation instance
            reservation = Reservation(
                size=size,
                comments=comments,
                tableNo=table,
                startTime=start_time,
                endTime=end_time,
                duration=duration,
                customer_name=customer_name,
                reservation_date=date
            )

            # Generate unique reservation ID
            reservation.reservationId = Reservation.generateReservationID()

            # Save the newly created reservation
            reservation.save()

            # Display success message and redirect
            messages.success(request, "Reservation added successfully!")
            context = {
                'media_url': settings.MEDIA_URL,  # Passing MEDIA_URL to template
            }
            return render(request, "managers/reserve_table.html", context)

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            
    # If request is not POST, render the reservation form page
    context = {
        'media_url': settings.MEDIA_URL,  # Passing MEDIA_URL to template
    }
    return render(request, "managers/reserve_table.html", context)

#Function to fetch reservation booking details for ammendment
def fetch_reservation_details(request, tableId):
    try:
        # Get the table instance
        table = get_object_or_404(Table, tableNo=tableId)

        # Fetch the latest reservation for the given table
        reservation = Reservation.objects.filter(tableNo=table).order_by('-reservation_date', '-endTime').first()
        
        if reservation:
            # Prepare reservation details in JSON format
            data = {
                "success": True,
                "reservationId": reservation.reservationId,
                "size": reservation.size,
                "comments": reservation.comments,
                "startTime": reservation.startTime,
                "endTime": reservation.endTime,
                "customerName": reservation.customer_name,
                "reservationDate": reservation.reservation_date,
                "capacity": table.capacity
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"success": False, "message": "No reservation found for this table."})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
        
#Function to ammend table reservation details
def ammend_reservation(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
    
    if request.method == "POST":
        #Retrieve form inputs
        reservation_id = request.POST.get("reservationID")
        customer_name = request.POST.get("upd-customer-name")
        reservation_date = request.POST.get("upd-reservationDate")
        fromTime = request.POST.get("upd-reservationStartTime")
        toTime = request.POST.get("upd-reservationEndTime")
        duration = request.POST.get("upd-reservationDuration")
        size = request.POST.get("upd-reservationSize")
        comments = request.POST.get("upd-reservationComments")

        #Obtain the specific reservation to be ammended
        try:
            reservation = Reservation.objects.get(reservationId=reservation_id)
            reservation.size = size
            reservation.customer_name = customer_name
            reservation.comments = comments
            reservation.reservation_date = reservation_date
            reservation.startTime = fromTime
            reservation.endTime = toTime
            reservation.duration = duration
            reservation.save()
            
            #Display success message
            messages.success(request, "Reservation details have been updated successfully!")
            
        except Reservation.DoesNotExist:
            messages.error(request, "Reservation does not exist.")

    context = {
        'media_url': settings.MEDIA_URL,
        'manager': manager
    }

    return render(request, "managers/reserve_table.html", context)

#Function to cancel booking/reservation
@csrf_exempt 
def cancelReservation(request, reservationId):
    if request.method == "POST":
        try:            
            # Retrieve the reservation by ID
            reservation = get_object_or_404(Reservation, reservationId=reservationId)
            
            print(f"{reservation}")
            # Get the associated table from the reservation
            table = reservation.tableNo  # Assuming tableNo is a ForeignKey to Table
            
            # Update table status to 'available'
            table.status = "available"
            table.save()

            # Delete the reservation
            reservation.delete()

            return JsonResponse({"success": "Reservation cancelled successfully"})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

#Function which displays the manager menu management interface
def displayMenuManagement(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
     
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        "manager": manager,
    }
    return render(request, 'managers/menu_management.html', context)

#Function which displays the add menu item form
def displayAddMenuItem(request):
    manager_id = request.session.get("manager_id")
    manager = Manager.objects.get(managerId=manager_id)
    food = Food.objects.all()
    drinks = Drink.objects.all()
     
    context = {
        'media_url': settings.MEDIA_URL,  # Passing the MEDIA_URL to the template
        "manager": manager,
        'food': food,
        'drinks': drinks
    }
    return render(request, 'managers/add_menu_item.html', context)


















