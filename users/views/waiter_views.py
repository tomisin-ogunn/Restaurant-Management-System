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

