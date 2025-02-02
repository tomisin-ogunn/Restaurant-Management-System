from django.db import models
from users.models import Waiter

# Create your models here.

#Model holding table information
class Table(models.Model):
    tableNo = models.CharField(max_length=10, unique=True, primary_key=True)
    capacity = models.IntegerField()
    waiter = models.ForeignKey(Waiter, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('reserved', 'Reserved')],
            default='available')
    
    #Displays table view of model in Django Admin
    def __str__(self):
        return f"Table {self.tableNo} - {self.status}"