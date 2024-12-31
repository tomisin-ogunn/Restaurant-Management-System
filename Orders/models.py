from django.db import models

# Create your models here.

#Model holding Orders information
class Order(models.Model):
    orderID = models.CharField(max_length=50, unique=True, primary_key=True)
    tableNo = 'test'
    order_placed_at = models.DateTimeField()
    notes = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    customerId = 'test'
    waiterId = 'test'
    customer_name = models.CharField(max_length=50)
    delivered_at = models.DateTimeField()
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.orderID}: {self.tableNo} {self.order_placed_at} {self.status}"
    
#Model holding Order items information
class OrderItem(models.Model):
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    foodId = 'test'
    drinkId = 'test'
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.orderID}: {self.foodId} {self.drinkId} {self.price}"