from django.db import models

# Create your models here.

#Abstract super class Product
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)
    
    class Meta:
        abstract = True

#Model holding information of Food table, inherits properties from abstract 'Products' superclass
class Food(Product):
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    duration = models.CharField(max_length=50)
    allergen = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
#Model holding information of Drink table, inherits properties from abstract 'Products' superclass
class Drink(Product):
    image = models.ImageField(upload_to='drink_images/', blank=True, null=True)
    description = models.CharField(max_length=100)    
    alcoholConc = models.CharField(max_length=100)    
    
    def __str__(self):
        return self.name
