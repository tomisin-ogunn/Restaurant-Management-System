from django.db import models
from Customers.models import Customer 
from Waiters.models import Waiter
from Tables.models import Table
from Products.models import Food, Drink

# Create your models here.

#Model holding Orders information
class Order(models.Model):
    orderID = models.CharField(max_length=50, unique=True, primary_key=True)
    tableNo = models.ForeignKey(Table, null=True, blank=True, on_delete=models.SET_NULL)
    order_placed_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    customerId = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    waiterId = models.ForeignKey(Waiter, null=True, blank=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=50)
    delivered_at = models.DateTimeField(auto_now_add=True)
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.orderID}: {self.tableNo} {self.order_placed_at} {self.status}"
    
#Model holding Order items information
class OrderItem(models.Model):
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    foodID = models.ForeignKey(Food, null=True, blank=True, on_delete=models.SET_NULL)
    drinkID = models.ForeignKey(Drink, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.orderID}: {self.foodID} {self.drinkID} {self.price}"