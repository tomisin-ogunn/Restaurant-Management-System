"""
URL configuration for RMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from restaurant.views import kitchen_views
from . import views
from users.views import manager_views, waiter_views, customer_views
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

#Url patterns for kitchen actions
urlpatterns = [
    path('kitchen-zone/<int:zoneID>/', kitchen_views.displayKitchenZone, name='kitchen_zone_detail'),
    path('get-kitchen-orders/<int:zoneID>/', kitchen_views.get_kitchen_orders, name='get_kitchen_orders'),  
    path('kitchen-zone-pending/<int:zoneID>/', kitchen_views.displayKitchenPendingOrders, name='kitchen_zone_pending'),
    path('completeOrder/<str:orderID>/<int:zoneID>/', kitchen_views.completeOrder, name="completeOrder"),
    path('get-active-orders-count/<int:zoneID>/', kitchen_views.get_active_orders_count, name='get_active_orders_count')
]
