import uuid
from django.db import models
from users.models import Waiter
from django.db.models import Max
from users.models import Customer
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
        return f"Table: {self.tableNo} - {self.status}, {self.capacity}"
    
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
        return f"Reservation: {self.reservationId} - {self.size}, {self.tableNo}, {self.duration}, {self.time_booked}"

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
        ('Deserts', 'Deserts')
    ]
    
    foodId = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=50, choices=FOOD_CATEGORIES ,default='Main Meal')       
    duration = models.CharField(max_length=10)
    price = models.CharField(max_length=10)        
    allergen = models.CharField(max_length=50, blank=True, null=True)        
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)   
    calories = models.CharField(max_length=10, null=True, blank=True)
    fav_status = models.CharField(max_length=50, blank=True, null=True)
    
    #Displays the table view of the model in Django Admin
    def __str__(self):
        return f"FoodId: {self.foodId} - {self.food_name}, {self.price}"
    
#Model holding Drinks information
class Drink(models.Model):
    DRINK_CATEGORIES = [
        ('Alcohol', 'Alcohol'),
        ('Soft Drinks', 'Soft Drinks'),
        ('Shakes', 'Shakes')
    ]
    
    drinkId = models.AutoField(primary_key=True)
    drink_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    alcoholConc = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=10)
    image = models.ImageField(upload_to='drink_images/', blank=True, null=True)        
    category = models.CharField(max_length=50, choices=DRINK_CATEGORIES ,default='Soft Drinks')
    calories = models.CharField(max_length=10, blank=True, null=True)     
    fav_status = models.CharField(max_length=50, blank=True, null=True)
    
    #Displays the table view of the model in Django Admin
    def __str__(self):
        return f" DrinkId: {self.drinkId} - {self.drink_name}, {self.price}"
    
#model holding Customers Favourites
class Favourite(models.Model):
    favourite_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    food_id = models.ForeignKey(Food, blank=True, null=True, on_delete=models.SET_NULL)
    drink_id = models.ForeignKey(Drink, blank=True, null=True, on_delete=models.SET_NULL)
            
    #Displays table view of model in Django Admin
    def __str__(self):
        return f"FavouriteId: {self.favourite_id} - {self.customer_id}, {self.food_id}, {self.drink_id}"
        
#Model holding basket information for users
class Basket(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    waiter = models.ForeignKey(Waiter, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True, null=True, blank=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def get_items(self):
        """Returns all order items in this basket."""
        return self.orderitem_set.all()

    def get_total_price(self):
        """Calculates the total price of the basket."""
        return sum(item.total_price for item in self.get_items())
    
    def __str__(self):
        return f"Basket {'for ' + str(self.user) if self.user else 'session ' + str(self.session_id)}"

#Model holding order items for users
class OrderItem(models.Model):
    basket = models.ForeignKey(Basket,  on_delete=models.SET_NULL, null=True, blank=True)
    food_item = models.ForeignKey(Food, null=True, blank=True, on_delete=models.SET_NULL)
    drink_item = models.ForeignKey(Drink, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.CharField(max_length=10)
    spice_level = models.CharField(max_length=50, choices=[('Not Spicy', 'Not Spicy'), ('Spicy', 'Spicy'), ('Very Spicy', 'Very Spicy')],
            null=True, blank=True)
    soup_choice = models.CharField(max_length=50, choices=[('Egusi', 'Egusi'), ('Ogbono', 'Ogbono'), ('Abula', 'Abula')],
            null=True, blank=True)
    food_sauce = models.CharField(max_length=50, choices=[('Ketchup', 'Ketchup'), ('Mayo', 'Mayo'), ('Sweet Chilli', 'Sweet Chilli')],
            null=True, blank=True)
    protein = models.CharField(max_length=50, choices=[('Chicken', 'Chicken'), ('Beef', 'Beef'), ('Fish', 'Fish')],
            null=True, blank=True)
    desert_sauce = models.CharField(max_length=50, choices=[('Toffee', 'Toffee'), ('Caramel', 'Caramel'), ('Strawberry', 'Strawberry')],
            null=True, blank=True)
    drink_size = models.CharField(max_length=50, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')],
            null=True, blank=True)
    has_ice = models.BooleanField(default=False)
    notes = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        item_name = self.food_item.food_name if self.food_item else self.drink_item.drink_name if self.drink_item else "Unknown Item"
        return f"{item_name} x {self.price}"

#Model holding Customer Ratings information
class Rating(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=50, null=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.CharField(max_length=10)
    comments = models.CharField(max_length=255, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)

#Model holding Orders information
class Order(models.Model):
    orderId = models.CharField(max_length=100, primary_key=True, blank=True, unique=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    placed_at = models.DateTimeField(auto_now_add=True)
    total_expected_duration = models.CharField(max_length=50) 
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=60)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Delayed', 'Delayed'), ('Ready', 'Ready'), ('Delivered', 'Delivered')],
            default='Pending')
    order_items = models.ManyToManyField(OrderItem, related_name='orders')
    
    #Function to increment reservation id after record has been added manually to the Orders.
    def save(self, *args, **kwargs):
        # Generate a reservationId if not already set
        if not self.orderId:
            self.orderId = self.generateOrderID()

        # Save the model instance
        super().save(*args, **kwargs)
    
    #Displays table view of model in Django Admin
    def __str__(self):
        return f"Order {self.orderId} - {self.table}, {self.customer_name}, {self.status}"

    #Function to generate a reservation id after appending
    @classmethod
    def generateOrderID(cls):
        # Prefix of reservation id
        
        prefix = 'JJ'
        
        #Obtains maximum current ID no from model
        last_order = Order.objects.all().aggregate(Max('orderId'))

        # Extract the current max number, or default to 0 if no records exist
        last_order_id = last_order.get('orderId__max', None)
        
        #Start from 000001
        if not last_order_id:
            new_order_number = 1
        else:
            #Extract number from last order id (00000x)
            last_number = int(last_order_id[6:])
            new_order_number = last_number + 1
            
        #Format the new reservation ID with prefix and 6 digit number
        new_order_id = f"{prefix}{new_order_number:06d}"
        
        return new_order_id

#Model holding KitchenZone(models.Model):
class KitchenZone(models.Model):
    zoneId = models.AutoField(primary_key=True)
    active_orders = models.PositiveIntegerField(default=0)
    total_remaining_time = models.PositiveBigIntegerField(default=0)

    #Displays table view of model in Django Admin
    def __str__(self):
        return f"Zone {self.zoneId} - Active Orders:{self.active_orders}, Remaining_Cooking_Time: {self.total_remaining_time}"
    
    @property
    def is_overloaded(self):
        """Check if the zone is overloaded (has 3 orders or more)."""
        return self.active_orders >= 3




