from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models import Max

# Create your models here.

#Model holding customers information
class Customer(models.Model):
    customerId = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
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
            
    # Function to provide 8 characters including 5 digits(starting 00001 incremented) with prefix 'JJC' to the manager ID
    @classmethod
    def generateCustomerID(cls):
        # Prefix of customer id
        
        prefix = 'JJC'
        
        #Obtains maximum current ID no from model
        last_customer = Customer.objects.all().aggregate(Max('customerId'))

         # Extract the current max number, or default to 0 if no records exist
        last_customer_id = last_customer.get('customerId__max', None)
        
        #Start from 0001
        if last_customer_id is None:
            new_customer_number = 1
        else:
            #Extract number from last customer id (0000x)
            last_number = int(last_customer_id[4:])
            new_customer_number = last_number + 1
            
        #Format the new customer ID with prefix and 5 digit number
        new_customer_id = f"{prefix}{new_customer_number:05d}"
        
        return new_customer_id
    
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.customerId}: {self.first_name} {self.last_name}"
            
            
            
                    
            
            
            
            
            
            
            
            
            