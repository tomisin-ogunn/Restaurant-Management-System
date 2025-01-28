from django.db import models

# Create your models here.

# Model (Table) holding managers information

class Manager(models.Model):
    managerId = models.CharField(max_length=10, unique=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=50)
    
#Model holding waiters information
class Waiter(models.Model):
    waiterId = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)