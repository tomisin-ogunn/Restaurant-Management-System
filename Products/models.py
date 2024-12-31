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
    foodID = models.CharField(max_length=20, unique=True, primary_key=True, default=1)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    duration = models.CharField(max_length=50)
    allergen = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=100)
    calories = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name
    
#Model holding information of Drink table, inherits properties from abstract 'Products' superclass
class Drink(Product):
    drinkID = models.CharField(max_length=20, unique=True, primary_key=True, default=1)
    image = models.ImageField(upload_to='drink_images/', blank=True, null=True)
    description = models.CharField(max_length=100)    
    alcoholConc = models.CharField(max_length=10)    
    
    def __str__(self):
        return self.name


#Model holding inventory (stock) information
class Inventory(models.Model):
    itemID = models.CharField(max_length=20, unique=True, primary_key=True)
    description = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('in_stock', 'In Stock'), ('low', 'Low'), ('out_of_stock', 'Out of Stock')])
    last_updated = models.CharField(max_length=50)
    updated_by = models.DateTimeField()
    foodID = models.ForeignKey(Food, on_delete=models.CASCADE)
    drinkID = models.ForeignKey(Drink, on_delete=models.CASCADE)





