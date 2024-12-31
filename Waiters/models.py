from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models import Max

# Create your models here.

#Model holding waiters information
class Waiter(models.Model):
    waiterId = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    
     # Function to hash the password for each manager, with parameters to allow additional positional and keyword arguements
    def hashPassword(self, *args, **kwargs):
        # Ensures passwords are not re-hashed by running checks
        
        # Checks if password exists and does not start with Django hashed password prefix
        if self.password and not self.password.startswith("pbkdf2_"):
            #Hashes the password
            self.password = make_password(self.password)
            #Calls the parent class's save method
            super().save(*args, **kwargs)
            
    # Function to provide 7 characters including 4 digits(starting 0001 incremented) with prefix 'JJW' to the waiter ID        
    @classmethod
    def generateWaiterID(cls):
        # Prefix of waiter id
        
        prefix = 'JJW'
        
        #Obtains maximum current ID no from model
        last_waiter = Waiter.objects.all().aggregate(Max('waiterId'))

         # Extract the current max number, or default to 0 if no records exist
        last_waiter_id = last_waiter.get('waiterId__max', None)
        
        #Start from 0001
        if last_waiter_id is None:
            new_waiter_number = 1
        else:
            #Extract number from last waiter id (000x)
            last_number = int(last_waiter_id[3:])
            new_waiter_number = last_number + 1
            
        #Format the new customer ID with prefix and 4 digit number
        new_waiter_id = f"{prefix}{new_waiter_number:04d}"
        
        return new_waiter_id
    
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.waiterId}: {self.first_name} {self.last_name}"
                
            
    