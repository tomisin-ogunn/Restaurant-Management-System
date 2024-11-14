from django.shortcuts import render

# Create your views here.

#Function to display Restaurant Manager login page

def display_managerlogin(request):
    return render(request, 'manager/login.html')