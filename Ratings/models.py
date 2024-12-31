from django.db import models
from Tables.models import Table
from Customers.models import Customer 

# Create your models here.

#Model holding ratings information
class Rating(models.Model):
    ratingID = models.CharField(max_length=20, unique=True, primary_key=True)
    tableNo = models.ForeignKey(Table, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    comments = models.CharField(max_length=100)
    submission_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.ratingID}: {self.customer} {self.score} {self.tableNo} {self.comments}"