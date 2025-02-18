from django.db import models
from users.models import Waiter
from django.db.models import Max
from django.utils import timezone
from django.utils.timezone import now, make_aware
from datetime import datetime


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
        return f"Table {self.tableNo} - {self.status}, {self.capacity}"
    
#Model holding reservation information
class Reservation(models.Model):
    reservationId = models.CharField(max_length=10, unique=True, blank=True, primary_key=True)
    size = models.IntegerField()
    comments = models.CharField(max_length=30)
    tableNo = models.ForeignKey(Table, blank=True, null=True, on_delete=models.SET_NULL)
    duration = models.CharField(max_length=20)
    time_booked = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=50)
    reservation_date = models.CharField(max_length=50)
    startTime = models.CharField(max_length=50)
    endTime = models.CharField(max_length=50)

    #Function to increment reservation id after record has been added manually to the Reservations table.
    def save(self, *args, **kwargs):
        # Generate a reservationId if not already set
        if not self.reservationId:
            self.reservationId = self.generateReservationID()

        # Save the model instance
        super().save(*args, **kwargs)
    
    #Displays table view of model in Django Admin
    def __str__(self):
        return f"Reservation {self.reservationId} - {self.size}, {self.tableNo}, {self.duration}, {self.time_booked}"

    #Function to generate a reservation id after appending
    @classmethod
    def generateReservationID(cls):
        # Prefix of reservation id
        
        prefix = 'RR'
        
        #Obtains maximum current ID no from model
        last_reservation = Reservation.objects.all().aggregate(Max('reservationId'))

         # Extract the current max number, or default to 0 if no records exist
        last_reservation_id = last_reservation.get('reservationId__max', None)
        
        #Start from 0001
        if not last_reservation_id:
            new_reservation_number = 1
        else:
            #Extract number from last reservation id (000x)
            last_number = int(last_reservation_id[3:])
            new_reservation_number = last_number + 1
            
        #Format the new reservation ID with prefix and 4 digit number
        new_reservation_id = f"{prefix}{new_reservation_number:04d}"
        
        return new_reservation_id

    #Function which automaically updates reservation status, based on current time (time elapsed)
    @property
    def time_elapsed(self):
        now_datetime = now()
    
        # Convert reservation_date (string) to a date object
        reservation_date_obj = datetime.strptime(self.reservation_date, "%Y-%m-%d").date()

        # Convert endTime (string) to a time object
        end_time_obj = datetime.strptime(self.endTime, "%H:%M").time()

        reservation_datetime = datetime.combine(reservation_date_obj, end_time_obj)
        
        # Make the datetime object timezone-aware using the same timezone as now()
        reservation_datetime = make_aware(reservation_datetime)
        
        if now_datetime > reservation_datetime:  # Check if reservation is expired
            table = self.tableNo
            
            future_reservations = Reservation.objects.filter(
                tableNo=table, 
                reservation_date__gte=self.reservation_date,  # Same or future date
                endTime__gt=self.endTime  # Ends after this reservation
            )

            if not future_reservations.exists() and table.status == "reserved":
                table.status = "available"
                table.save()
                return True  # Expired & status updated
            

        return False  # Not expired
            
#Model holding food information
class Food(models.Model):
    FOOD_CATEGORIES = [
        ('Main Meal', 'Main Meal'),
        ('Fast Food', 'Fast Food'),
        ('Sides', 'Sides'),
    ]
    
    foodId = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, choices=FOOD_CATEGORIES ,default='Main Meal')       
    duration = models.CharField(max_length=10)
    price = models.CharField(max_length=10)        
    allergen = models.CharField(max_length=50, blank=True, null=True)        
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)        
    
    #Displays the table view of the model in Django Admin
    def __str__(self):
        return f"Table {self.foodId} - {self.food_name}, {self.price}, {self.ingredients}"
    
#Model holding Drinks information
class Drink(models.Model):
    DRINK_CATEGORIES = [
        ('Alcohol', 'Alcohol'),
        ('Soft Drinks', 'Soft Drinks'),
        ('Shakes', 'Shakes')
    ]
    
    drinkId = models.AutoField(primary_key=True)
    drink_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    alcoholConc = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    image = models.ImageField(upload_to='drink_images/', blank=True, null=True)        
    category = models.CharField(max_length=50, choices=DRINK_CATEGORIES ,default='Soft Drinks')     
    
    #Displays the table view of the model in Django Admin
    def __str__(self):
        return f"Table {self.drinkId} - {self.drink_name}, {self.description}, {self.price}"
    
    
    
    
            
            
            
        