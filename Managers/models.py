from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db.models import Max

# Create your models here.

# Model (Table) holding managers information

class Manager(models.Model):
    managerId = models.CharField(max_length=10, unique=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=50)
    
    USERNAME_FIELD = 'managerId'
    REQUIRED_FIELDS = []
    
    # Function to hash the password for each manager, with parameters to allow additional positional and keyword arguements
    def hashPassword(self, *args, **kwargs):
        # Ensures passwords are not re-hashed by running checks
        
        # Checks if password exists and does not start with Django hashed password prefix
        if self.password and not self.password.startswith("pbkdf2_"):
            #Hashes the password
            self.password = make_password(self.password)
            #Calls the parent class's save method
            super().save(*args, **kwargs)
    
    #Function to hash password and increment manager Id after record has been added manually to Managers table
    def save(self, *args, **kwargs):
        # Call hashPassword before saving the model
        self.hashPassword(*args, **kwargs)
        # Save the model instance
        super().save(*args, **kwargs)
        
        # Automatically generate a managerId if not set or if manually inputted
        if not self.managerId:
            self.managerId = self.generateManagerID()
        super().save(*args, **kwargs)  # Call the parent class's save metho
    
    # Function to provide 7 characters including 4 digits(starting 0001 incremented) with prefix 'JJM' to the manager ID
    @classmethod
    def generateManagerID(cls):
        # Prefix of manager id
        
        prefix = 'JJM'
        
        #Obtains maximum current ID no from model
        last_manager = Manager.objects.all().aggregate(Max('managerId'))

         # Extract the current max number, or default to 0 if no records exist
        last_manager_id = last_manager.get('managerId__max', None)
        
        #Start from 0001
        if not last_manager_id:
            new_manager_number = 1
        else:
            #Extract number from last manager id (000x)
            last_number = int(last_manager_id[3:])
            new_manager_number = last_number + 1
            
        #Format the new manager ID with prefix and 4 digit number
        new_manager_id = f"{prefix}{new_manager_number:04d}"
        
        return new_manager_id
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.managerId}: {self.first_name} {self.last_name}"