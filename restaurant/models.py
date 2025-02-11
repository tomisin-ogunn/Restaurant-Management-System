from django.db import models
from users.models import Waiter
from django.db.models import Max
from django.utils import timezone

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
    reservation_date = models.DateTimeField(default=timezone.now)
    startTime = models.TimeField(default=timezone.now)
    endTime = models.TimeField(default=timezone.now)

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



