from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Manager

#Manager Login Authentication functionality
class ManagerAuthenticationBackend(BaseBackend):
    #Function to authenticate user
    def authenticate(self, request, managerId=None, password=None):
        try:
            manager = Manager.objects.get(managerId=managerId)
            #Verify the password
            if check_password(password, manager.password):
                return manager
        except Manager.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return Manager.objects.get(pk=user_id)
        except Manager.DoesNotExist:
            return None