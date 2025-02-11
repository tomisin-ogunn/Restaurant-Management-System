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
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

urlpatterns = [
    #Route for user views (manager)
    path('manager-login/', views.display_managerLogin, name="manager-login"),
    path('manager-home/', views.displayManagerHome, name="manager-home"),
    path('manager_verification/', views.manager_loginAuth, name="manager_ver"),
    path('manager-logout/', views.manager_logout, name="manager-logout"),
    path('manager_email_verifier', views.managerEmail_verifier, name='manager_email_verifier'),
    path('manager-update-password', views.update_ManagerPassword, name="manager-update-password"),
    path('manager-waiter-management/', views.displayWaiterManagement, name="manager-waiter-management"),
    path('manager-add-waiter/', views.displayWaiterAddForm, name="add-waiter"),
    path('manager-edit-waiter/', views.displayWaiterEditForm, name="edit-waiter"),
    path('append-waiter/', views.addWaiter, name="append-waiter"),
    path('get-waiter-details/<str:waiter_id>/', views.get_waiter_details, name='get_waiter_details'),
    path('update-waiter-details', views.updateWaiterDetails, name="update-waiter-details"),
    path('manager-assign-waiter/', views.displayAssignWaiterForm, name="assign-waiter"),
    path('assign-waiter-table/', views.assignWaiter, name="assign-waiter-table"),
    path('manager-table-reservation/', views.displayTableReservation, name="manager-table-reservation"),
    path('get-table-details/<str:tableId>/', views.get_table_details, name="get-table-details")
]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)