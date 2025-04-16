from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models import Max

# Create your models here.

# Model (Table) holding managers information
class Manager(models.Model):
    managerId = models.CharField(max_length=10, unique=True, blank=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=50)
    
    #Function to hash password 
    def hashPassword(self):
        # Hash the password using Django's built-in utility
        return make_password(self.password)
    
    #Function to hash password and increment manager Id after record has been added manually to Managers table
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = self.hashPassword()

        # Generate a managerId if not already set
        if not self.managerId:
            self.managerId = self.generateManagerID()

        # Save the model instance
        super().save(*args, **kwargs)
    
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
    
#Model holding waiters information
class Waiter(models.Model):
    waiterId = models.CharField(max_length=10, unique=True, blank=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    first_login = models.BooleanField(default=True)
    
    #Function to hash password 
    def hashPassword(self):
        # Hash the password using Django's built-in utility
        return make_password(self.password)
    
    #Function to hash password and increment waiter Id after record has been added to Waiters table
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password and not self.password.startswith('pbkdf2_'):  # Avoid rehashing
            self.password = self.hashPassword()

        # Generate a waiterId if not already set
        if not self.waiterId:
            self.waiterId = self.generateWaiterID()

        # Save the model instance
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
                
#Model holding customer information
class Customer(models.Model):
    customerId = models.CharField(max_length=10, unique=True, blank=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    
    #Function to hash password 
    def hashPassword(self):
        # Hash the password using Django's built-in utility
        return make_password(self.password)
    
    #Function to increment waiter Id after record has been added to Waiters table
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password and not self.password.startswith('pbkdf2_'): 
            self.password = self.hashPassword()

        # Generate a customerId if not already set
        if not self.customerId:
            self.customerId = self.generateCustomerID()

        # Save the model instance
        super().save(*args, **kwargs)
            
    # Function to provide 7 characters including 5 digits(starting 00001 incremented) with prefix 'JJC' to the customer ID        
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
            #Extract number from last waiter id (0000x)
            last_number = int(last_customer_id[4:])
            new_customer_number = last_number + 1
            
        #Format the new customer ID with prefix and 5 digit number
        new_customer_id = f"{prefix}{new_customer_number:05d}"
        
        return new_customer_id
    
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.customerId}: {self.first_name} {self.last_name}"   
                