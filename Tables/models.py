from django.db import models


# Create your models here.

#Model holding Table information
class Table(models.Model):
    tableNo = models.CharField(max_length=10, unique=True, primary_key=True)
    capacity = models.PositiveIntegerField()
    waiterId = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.tableNo}: {self.capacity} {self.waiterId} {self.status}"
    
#Model holding reservation information        
class Reservation(models.Model):
    reservationId = models.CharField(max_length=50, unique=True, primary_key=True)
    size = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=50)
    tableNo = models.ForeignKey(Table, on_delete=models.CASCADE)
    comments = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    time_booked = models.DateTimeField()
    customerId = models.CharField(max_length=50)
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.reservationId}: {self.tableNo} {self.size} {self.time_booked}"
    