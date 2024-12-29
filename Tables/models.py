from django.db import models

# Create your models here.

#Model holding Table information
class Table(models.Model):
    tableNo = models.CharField(max_length=10, unique=True)
    capacity = models.CharField(max_length=10)
    waiterId = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.tableNo}: {self.capacity} {self.waiterId} {self.status}"