from django.db import models

# Create your models here.

#Model holding ratings information
class Rating(models.Model):
    ratingID = models.CharField(max_length=50, unique=True)
    tableNo = models.CharField(max_length=50)
    score = models.CharField(max_length=50)
    comments = models.CharField(max_length=100)
    submission_date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=50)
    
    #Provides display of object in Django Admin/Shell
    def __str__(self):
        return f"{self.ratingID}: {self.score} {self.tableNo} {self.comments}"