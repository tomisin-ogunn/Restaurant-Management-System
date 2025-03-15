from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.utils import timezone
from .models import Manager, Waiter, Customer
from restaurant.models import Table, Reservation, Food, Drink, Basket, OrderItem
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import string
import secrets
import re


# # Create your views here.





