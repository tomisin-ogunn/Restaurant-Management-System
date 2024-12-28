from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

# Model (Table) holding managers information

class Manager(models.Model):
    managerId = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=50)
    
    # Function to hash the password for each manager, with parameters to allow additional positional and keyword arguements
    def hashPassword(self, *args, **kwargs):
        # Ensures passwords are not re-hashed by running checks
        
        # Checks if password exists and does not start with Django hashed password prefix
        if self.password and not self.password.startswith("pbkdf2_"):
            #Hashes the password
            self.password = make_password(self.password)
            #Calls the parent class's save method
            super().save(*args, **kwargs)
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.managerId}: {self.first_name} {self.last_name}"
            
            
            
            