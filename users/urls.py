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
from . import views
from users.views import manager_views, waiter_views, customer_views
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

urlpatterns = [
    #Route for user views (manager) authentication functionalities
    path('manager-login/', manager_views.display_managerLogin, name="manager-login"),
    path('manager-home/', manager_views.displayManagerHome, name="manager-home"),
    path('manager_verification/', manager_views.manager_loginAuth, name="manager_ver"),
    path('manager-logout/', manager_views.manager_logout, name="manager-logout"),
    path('manager_email_verifier', manager_views.managerEmail_verifier, name='manager_email_verifier'),
    path('manager-update-password', manager_views.update_ManagerPassword, name="manager-update-password"),
   
]

#Url Patterns for waiter management functionalities for managers
urlpatterns += [
    path('manager-waiter-management/', manager_views.displayWaiterManagement, name="manager-waiter-management"),
    path('manager-add-waiter/', manager_views.displayWaiterAddForm, name="add-waiter"),
    path('manager-edit-waiter/', manager_views.displayWaiterEditForm, name="edit-waiter"),
    path('append-waiter/', manager_views.addWaiter, name="append-waiter"),
    path('get-waiter-details/<str:waiter_id>/', manager_views.get_waiter_details, name='get_waiter_details'),
    path('update-waiter-details', manager_views.updateWaiterDetails, name="update-waiter-details"),
    path('manager-assign-waiter/', manager_views.displayAssignWaiterForm, name="assign-waiter"),
    path('assign-waiter-table/', manager_views.assignWaiter, name="assign-waiter-table"),
]

#Url Patterns for table reservation funcionalities for managers
urlpatterns += [
    path('manager-table-reservation/', manager_views.displayTableReservation, name="manager-table-reservation"),
    path('get-table-details/<str:tableId>/', manager_views.get_table_details, name="get-table-details"),
    path('get-reservation-details/<str:tableId>/', manager_views.fetch_reservation_details, name="get-reservation-details"),
    path('create-reservation', manager_views.generateReservation, name="create-reservation"),
    path('update-reservation', manager_views.ammend_reservation, name="update-reservation"),
    path('cancelReservation/<str:reservationId>/', manager_views.cancelReservation, name="cancelReservation"),
]

#Url Patterns for menu management functionality for managers
urlpatterns += [
    path('manager-menu-management', manager_views.displayMenuManagement, name="manager-menu-management"),
    path('add-menu-item', manager_views.displayAddMenuItem, name="add-menu-item"),
    path('append-menu-item', manager_views.addMenuItem, name="append-menu-item"),
    path('manager-menu-items', manager_views.displayMenuItems, name="manager-menu-items"),
    path('removeMenuItem/<str:itemId>/<str:itemType>/', manager_views.removeMenuItem, name="removeMenuItem"),
    path('fetch-item-details/<str:itemID>/<str:itemType>/', manager_views.fetchItemDetails, name="fetch-item-details"),
    path('updateFoodItem', manager_views.updateFoodItem, name="updateFoodItem"),
    path('updateDrinkItem', manager_views.updateDrinkItem, name="updateDrinkItem")
]

#Url Patterns for Waiter Authentication Functionalities
urlpatterns += [
    path('waiter-login/', waiter_views.displayWaiterLogin, name="waiter-login" ),
    path('waiter-authentication', waiter_views.waiter_loginAuth, name="waiter-auth"),
    path('waiter-home/', waiter_views.displayWaiterHome, name="waiter-home"),
    path('update-waiter-password', waiter_views.updateWaiterPassword, name="update-waiter-password"),
    path('waiter-id-ver', waiter_views.waiterID_verifier, name="waiter-id-ver"),
    
]

#Url Patterns for Waiter actions/functionalities
urlpatterns += [
    path('waiter-basket/', waiter_views.displayBasketWaiter, name="waiter-basket"),
    path('addItemToBasketWaiter/<str:itemID>/<str:itemType>/', waiter_views.addToBasketWaiter, name="addItemToBasketWaiter"),
    path('removeItemFromBasketWaiter/<str:itemID>/', waiter_views.removeBasketItemWaiter, name="removeItemFromBasketWaiter"),
    path('deleteBasketItemsWaiter/', waiter_views.deleteBasketItemsWaiter, name="deleteBasketItemsWaiter"),
    path('fetch-order-item-details-waiter/<str:itemID>/', waiter_views.fetchOrderItemDetailsWaiter, name="fetch-order-item-details-waiter"),
    path('generateOrderWaiter/', waiter_views.generateOrderWaiter, name="generateOrderWaiter"),
    path('waiter-logout', waiter_views.waiterLogOut, name="waiter-logout"),
    path('waiter-notifications/', waiter_views.displayWaiterNotifications, name="waiter-notifications")
]

#Url patterns for Customer Authentication Functionalities
urlpatterns += [
    path('customer-login/', customer_views.displayCustomerLogin, name="customer-login"),
    path('customer-auth', customer_views.customer_loginAuth, name="customer-auth"),
    path('customer-loggedIn-home/', customer_views.displayCustomerLoggedInHome, name="customer-loggedIn-home"),
    path('customer-email-ver', customer_views.customerEmail_verifier, name="customer-email-ver"),
    path('update-customer-password', customer_views.update_CustomerPassword, name="update-customer-password"),
    path('customer-register/', customer_views.displayCustomerRegister, name="customer-register"),
    path('customer-registration', customer_views.appendCustomer, name="customer-registration"),
    path('customer-logout', customer_views.customerLogOut, name="customer-logout"),
    path("regenerate-session/", customer_views.regenerate_session, name="regenerate-session")
]

#Url patterns for customer actions 
urlpatterns += [
    path('customer-home/', customer_views.displayCustomerHome, name="customer-home"),
    path('addItemToFavourites/<str:itemID>/<str:itemType>/', customer_views.addItemToFavourites, name="addItemToFavourites"),
    path('customer-favourites/', customer_views.displayCustomerFavourites, name="customer-favourites"),
    path('removeItemFromFavourites/<str:itemID>/<str:itemType>/',  customer_views.removeItemFromFavourites, name="removeItemFromFavourites"),
    path('addItemToBasket/<str:itemID>/<str:itemType>/', customer_views.addToBasket, name="addItemToBasket"),
    path('addItemToBasketCustomer/<str:itemID>/<str:itemType>/', customer_views.addToBasketCustomer, name="addItemToBasketCustomer"),
    path('user-basket/', customer_views.displayBasket, name="user-basket"),
    path('removeItemFromBasket/<str:itemID>/', customer_views.removeBasketItem, name="removeItemFromBasket"),
    path('customer-rating/', customer_views.displayCustomerRatingForm, name="customer-rating"),
    path('createCustomerRating', customer_views.createCustomerRating, name="createCustomerRating"),
    path('deleteBasketItems/', customer_views.deleteBasketItems, name="deleteBasketItems"),
    path('deleteBasketItemsCustomer/', customer_views.deleteBasketItemsCustomer, name="deleteBasketItemsCustomer"),
    path('fetch-order-item-details/<str:itemID>/', customer_views.fetchOrderItemDetails, name="fetch-order-item-details"),
    path('generateOrder/', customer_views.generateOrder, name="generateOrder"),
    path('generateOrderCustomer/', customer_views.generateOrderCustomer, name="generateOrderCustomer"),
    path('customer-basket', customer_views.displayCustomerBasket, name="customer-basket"),
    path('customer-loggedIn-rating/', customer_views.displayCustomerLoggedInRatingForm, name="customer-loggedIn-rating")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







