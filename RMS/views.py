from django.http import HttpResponse
from django.shortcuts import render

#Function to display home page of project
def display_homepage(request):
    return render(request, 'home.html')