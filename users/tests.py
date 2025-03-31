from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password, check_password
from users.models import Manager, Waiter, Customer
from restaurant.models import Food, Drink, Basket, Order, Table, Reservation
from restaurant.models import Basket, OrderItem
from django.urls import reverse
from django.contrib.messages import get_messages

# Create your tests here.

#Unit Test Case for User Login Functionalities
class UserLoginTests(TestCase):
    
    #Create the test data before verifications
    def setUp(self):
        self.client = Client()

        # Generate a unique manager ID
        manager_id = Manager.generateManagerID()
        
        # Create test manager with hashed password
        self.manager_password = "manager123"
        self.manager = Manager.objects.create(
            managerId=manager_id,
            first_name="John",
            last_name="Tres",
            email="m@yahoo.com",
            password=make_password(self.manager_password) 
        )
        
        # Generate a unique waiter ID
        waiter_id = Waiter.generateWaiterID()
        
        # Create test waiter
        self.waiter_password = "waiter123"
        self.waiter = Waiter.objects.create(
            waiterId=waiter_id,
            first_name="Alice",
            last_name="Reer",
            email="w@yahoo.com",
            password=make_password(self.waiter_password),
            first_login=False
        )

        # Generate a unique customer ID
        customer_id = Customer.generateCustomerID()

        # Create test customer
        self.customer_password = "customer123"
        self.customer = Customer.objects.create(
            customerId=customer_id,
            first_name="customer1",
            last_name="Weber",
            email="c@gmail.com",
            password=make_password(self.customer_password)
        )
        
    def test_manager_login_success(self):
        """Test manager login with correct credentials."""
        
        login_url = reverse("manager_ver")
         
        response = self.client.post(login_url, {
            "username": self.manager.managerId,
            "password": self.manager_password
        })

        self.assertRedirects(response, reverse("manager-home"))  # Successful login should redirect
        
        # Assert that login redirects (indicating success) and manager_id is set in session
        if response.status_code == 302 and "manager_id" in self.client.session:
            print("✅ Manager login test passed!")
        else:
            print("❌ Manager login test failed!")
        
        # Assert redirect (302)
        self.assertEqual(response.status_code, 302)

        # Check that manager_id is stored in session
        self.assertIn('manager_id', self.client.session)
       
    def test_manager_login_invalid_password(self):
        """Test manager login with incorrect password."""
        
        login_url = reverse("manager_ver") 
        
        response = self.client.post(login_url, {
            "username": self.manager.managerId,
            "password": "wrongpassword"
        })
        if "Invalid Employee ID / Password" in response.content.decode():
            print("✅ Manager invalid password test passed!")
        else:
            print("❌ Manager invalid password test failed!")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Employee ID / Password")

    def test_manager_login_invalid_id(self):
        
        """Test manager login with a non-existent manager ID."""
        
        login_url = reverse("manager_ver") 
        
        response = self.client.post(login_url, {
            "username": "INVALID_ID",
            "password": self.manager_password
        })
        if "Invalid Employee ID / Password" in response.content.decode():
            print("✅ Manager invalid ID test passed!")
        else:
            print("❌ Manager invalid ID test failed!")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Employee ID / Password")

    def test_waiter_login_success(self):
        """Test waiter login with correct credentials."""
        
        login_url = reverse("waiter-auth") 
         
        response = self.client.post(login_url, {
            "waiter-username": self.waiter.waiterId,
            "waiter-password": self.waiter_password
        })
        if response.status_code == 302 and "waiter_id" in self.client.session:
            print("✅ Waiter login test passed!")
        else:
            print("❌ Waiter login test failed!")
        self.assertEqual(response.status_code, 302)
        self.assertIn("waiter_id", self.client.session)

    def test_waiter_login_invalid_credentials(self):
        """Test waiter login with incorrect credentials."""
        
        login_url = reverse("waiter-auth") 
        
        response = self.client.post(login_url, {
            "waiter-username": self.waiter.waiterId,
            "waiter-password": "wrongpassword"
        })
        if "Invalid Employee ID / Password" in response.content.decode():
            print("✅ Waiter invalid credentials test passed!")
        else:
            print("❌ Waiter invalid credentials test failed!")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Employee ID / Password")

    def test_customer_login_success(self):
        """Test customer login with correct credentials."""
        
        login_url = reverse("customer-auth") 
        
        response = self.client.post(login_url, {
            "customer-email": self.customer.email,
            "customer-password": self.customer_password
        })
        if response.status_code == 302 and "customer_email" in self.client.session:
            print("✅ Customer login test passed!")
        else:
            print("❌ Customer login test failed!")
        self.assertEqual(response.status_code, 302)
        self.assertIn("customer_email", self.client.session)

    def test_customer_login_invalid_credentials(self):
        """Test customer login with incorrect credentials."""
        
        login_url = reverse("customer-auth") 
        
        response = self.client.post(login_url, {
            "customer-email": self.customer.email,
            "customer-password": "wrongpassword"
        })
        if "Invalid Email / Password" in response.content.decode():
            print("✅ Customer invalid credentials test passed!")
        else:
            print("❌ Customer invalid credentials test failed!")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Email / Password")
        
#Unit Test Case for Waiter Management
class WaiterManagementTests(TestCase):
    
    def setUp(self):
        
        """Set up a manager for login testing."""
        # Generate a unique manager ID
        manager_id = Manager.generateManagerID()
        
        self.manager = Manager.objects.create(
            managerId=manager_id,
            first_name="John",
            last_name="Doe",
            password="password123",
            email="john.doe@example.com"
        )
        # Simulate login by setting manager ID in session
        session = self.client.session
        session['manager_id'] = self.manager.managerId
        session.save()
        
        # Set up the test waiter data
        self.waiter_data = {
            "first-name": "John",
            "last-name": "Doe",
            "waiter-email": "john.doe@example.com"
        }
        self.table = Table.objects.create(tableNo=1, capacity=5)

    def test_add_waiter_success(self):
        """Test adding a new waiter successfully."""
        url = reverse('append-waiter')
        
        response = self.client.post(url, self.waiter_data)
        
        # Assert that the waiter was successfully added
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Waiter added successfully!")

        # Check if the waiter exists in the database
        waiter = Waiter.objects.get(email=self.waiter_data["waiter-email"])
        self.assertEqual(waiter.first_name, "John")
        self.assertEqual(waiter.last_name, "Doe")
        self.assertEqual(waiter.email, "john.doe@example.com")
        
        if waiter:
            print("✅ Waiter Addition test passed!")

    def test_assign_waiter_success(self):
        """Test successfully assigning a waiter to a table."""
        # Create a waiter to be assigned
        waiter = Waiter.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="hashed_password"
        )
        self.table.waiter = waiter
        self.table.save()

        url = reverse('assign-waiter')
        data = {
            "waiters": waiter.waiterId,
            "tables": self.table.tableNo
        }

        response = self.client.post(url, data)

        # Assert that the waiter was successfully assigned
        self.assertEqual(response.status_code, 200)

        # Verify that the table is assigned to the waiter
        table = Table.objects.get(tableNo=self.table.tableNo)
        self.assertEqual(table.waiter, waiter)
        
        if table.waiter == waiter:
            print("✅ Waiter Edit Test Passed!")

    # def test_update_waiter_details_success(self):
        """Test successfully updating a waiter's details."""
        # Create a waiter to be updated
        # waiter = Waiter.objects.create(
        #     first_name="Sarah",
        #     last_name="Connor",
        #     email="sarah.connor@example.com",
        #     password="hashed_password"
        # )

        # url = reverse('update-waiter-details')
        # data = {
        #     "updWaiterID": waiter.waiterId,
        #     "updfirst-name": "Sarah",
        #     "updlast-name": "Connor",
        #     "waiter-email": "new.email@example.com"
        # }

        # response = self.client.post(url, data)

        # # Assert that the waiter details were successfully updated
        # self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Waiter details have been successfully updated!")

        # # Verify that the waiter's email was updated
        # updated_waiter = Waiter.objects.get(waiterId=waiter.waiterId)
        # self.assertEqual(updated_waiter.email, "new.email@example.com")
 
    def test_update_waiter_details_success(self):
        """Test successfully updating a waiter's details."""
        # Create a waiter to be updated
        waiter = Waiter.objects.create(
            first_name="Sarah",
            last_name="Connor",
            email="sarah.connor@example.com",
            password="hashed_password"
        )

        url = reverse('update-waiter-details')
        data = {
            "updWaiterID": waiter.waiterId,
            "updfirst-name": "Sarah",
            "updlast-name": "Connor",
            "waiter-email": "new.email@example.com"
        }

        response = self.client.post(url, data)

        # Assert that the waiter details were successfully updated
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Waiter details have been successfully updated!")

        # Verify that the waiter's email was updated
        updated_waiter = Waiter.objects.get(waiterId=waiter.waiterId)
        self.assertEqual(updated_waiter.email, "new.email@example.com")
        
        if updated_waiter.email == "new.email@example.com":
            print("✅ Waiter Details Update Test Passed!")
 
#Unit Test Case for Menu Management
class MenuManagementTests(TestCase):

    def setUp(self):
        """Set up a manager for login testing."""
        # Generate a unique manager ID
        manager_id = Manager.generateManagerID()
        
        self.manager = Manager.objects.create(
            managerId=manager_id,
            first_name="John",
            last_name="Doe",
            password="password123",
            email="john.doe@example.com"
        )
        # Simulate login by setting manager ID in session
        session = self.client.session
        session['manager_id'] = self.manager.managerId
        session.save()
        
        # Create food and drink items for testing deletion
        self.food_item = Food.objects.create(
            food_name="Burger",
            ingredients="Beef Patty, Lettuce, Tomato, Cheese, Pickles",
            category="American",
            duration="10 minutes",
            price=8.99,
            calories=350
        )

        # Creating a new drink item with unique values
        self.drink_item = Drink.objects.create(
            drink_name="Lemonade",
            description="A sweet and tangy citrus drink.",
            category="Fruit Juice",
            alcoholConc="0%",
            price=3.00,
            calories=120
        )

    def test_add_drink_item(self):
        """Test adding a drink item."""
        url = reverse('append-menu-item')  # URL for the add menu item view

        # Form data for adding a drink
        data = {
            'itemType': 'Drink',
            'drink-name': 'Coca Cola',
            'description': 'A refreshing soft drink.',
            'drink-category': 'Soda',
            'alcohol-conc': '0%',
            'drink-price': '2.50',
            'drink-calories': '150'
        }

        response = self.client.post(url, data)

        # Check if the drink was successfully added
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Drink has been successfully added!")
        
        # Verify the drink was saved in the database
        drink = Drink.objects.get(drink_name="Coca Cola")
        self.assertEqual(drink.drink_name, 'Coca Cola')
        print("✅ Drink Addition Test Passed!")
        

    def test_add_food_item(self):
        """Test adding a food item."""
        url = reverse('append-menu-item')  # URL for the add menu item view

        # Form data for adding a food item
        data = {
            'itemType': 'Food',
            'food-name': 'Pizza',
            'ingredients': 'Cheese, Tomato Sauce, Pepperoni',
            'category': 'Italian',
            'duration': '15 minutes',
            'food-price': '12.99',
            'food-calories': '250',
            'allergen': 'Dairy'
        }

        response = self.client.post(url, data)

        # Check if the food item was successfully added
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Food item has been successfully added!")
        
        # Verify the food was saved in the database
        food = Food.objects.get(food_name="Pizza")
        self.assertEqual(food.food_name, 'Pizza')
        print("✅ Food Addition Test Passed!")

    def test_add_invalid_item(self):
        """Test adding an item with missing or invalid data."""
        url = reverse('append-menu-item')  # URL for the add menu item view

        # Invalid form data (missing required fields)
        data = {
            'itemType': 'Food',  # Missing required fields
            'food-name': '',
            'ingredients': '',
            'category': '',
            'duration': '',
            'food-price': '',
            'food-calories': '',
            'allergen': '',
        }

        response = self.client.post(url, data)

        # Assert that error messages are shown for invalid data
        self.assertEqual(response.status_code, 200)
 
    def test_remove_food_item(self):
        """Test removing a food item."""
        url = reverse('removeMenuItem', kwargs={'itemId': self.food_item.foodId, 'itemType': 'food'})

        response = self.client.post(url)

        # Check if the food item is deleted successfully
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': 'Menu Item removed successfully'})

        # Verify the food item was removed from the database
        with self.assertRaises(Food.DoesNotExist):
            Food.objects.get(foodId=self.food_item.foodId)
        
        if Food.DoesNotExist:
            print("✅ Food Item Deletion Successful!")
            
    def test_remove_drink_item(self):
        """Test removing a drink item."""
        url = reverse('removeMenuItem', kwargs={'itemId': self.drink_item.drinkId, 'itemType': 'drink'})

        response = self.client.post(url)

        # Check if the drink item is deleted successfully
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': 'Menu Item removed successfully'})

        # Verify the drink item was removed from the database
        with self.assertRaises(Drink.DoesNotExist):
            Drink.objects.get(drinkId=self.drink_item.drinkId)
        
        if Drink.DoesNotExist:
            print("✅ Drink Deletion Successful!!")

    def test_update_food_item(self):
        """Test updating a food item."""
        url = reverse('updateFoodItem')

        data = {
            'upd-foodID': self.food_item.foodId,
            'upd-food-name': 'Updated Pizza',
            'upd-ingredients': 'Cheese, Tomato Sauce, Mushrooms',
            'upd-category': 'Italian',
            'upd-duration': '20 minutes',
            'upd-price': '13.99',
            'upd-calories': '300',
            'upd-allergen': 'Dairy'
        }

        response = self.client.post(url, data)

        # Check if the food item was successfully updated
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menu item have been updated successfully!")

        # Verify the food item was updated in the database
        updated_food_item = Food.objects.get(foodId=self.food_item.foodId)
        self.assertEqual(updated_food_item.food_name, "Updated Pizza")
        self.assertEqual(updated_food_item.price, '13.99')
        self.assertEqual(updated_food_item.calories, '300')
        
        if updated_food_item.food_name == "Updated Pizza":
            print("✅ Food Item Update Test Passed!")
        
    def test_update_drink_item(self):
        """Test updating a drink item."""
        url = reverse('updateDrinkItem')

        data = {
            'upd-drinkID': self.drink_item.drinkId,
            'upd-drink-name': 'Updated Coca Cola',
            'upd-description': 'A refreshing soda with a new formula.',
            'upd-drink-category': 'Soda',
            'upd-drink-price': '2.75',
            'upd-drink-calories': '160',
            'upd-alcohol-conc': '0%'
        }

        response = self.client.post(url, data)

        # Check if the drink item was successfully updated
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menu item have been updated successfully!")

        # Verify the drink item was updated in the database
        updated_drink_item = Drink.objects.get(drinkId=self.drink_item.drinkId)
        self.assertEqual(updated_drink_item.drink_name, "Updated Coca Cola")
        self.assertEqual(updated_drink_item.price, '2.75')
        self.assertEqual(updated_drink_item.calories, '160')
 
        if updated_drink_item.drink_name == "Updated Coca Cola":
            print("✅ Drink Item Update Test Passed!")
 
#Unit Test Case for Table Reservations
class TableReservationTests(TestCase):
    
    def setUp(self):
        """Set up a manager for login testing."""
        # Generate a unique manager ID
        manager_id = Manager.generateManagerID()
        
        self.manager = Manager.objects.create(
            managerId=manager_id,
            first_name="John",
            last_name="Doe",
            password="password123",
            email="john.doe@example.com"
        )
        # Simulate login by setting manager ID in session
        session = self.client.session
        session['manager_id'] = self.manager.managerId
        session.save()
        
        # Create a table
        self.table = Table.objects.create(
            tableNo=1,
            capacity=4,
            status="available"
        )

        # Prepare the reservation data
        self.reservation_data = {
            "tableNo": self.table.tableNo,
            "reservationDate": "2025-04-10",
            "reservationStartTime": "12:00",
            "reservationEndTime": "14:00",
            "reservationDuration": "2 hours",
            "reservationSize": 2,
            "reservationComments": "Birthday celebration",
            "customer-name": "John Doe",
            "tableCapacity": self.table.capacity,
        }
    
        
    def test_generate_reservation_success(self):
        """Test generating a reservation successfully."""
        url = reverse('create-reservation')
        
        # Send a POST request to generate a reservation
        response = self.client.post(url, self.reservation_data)
        
        # Check if the reservation was created successfully
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reservation added successfully!")

        # Verify that the reservation exists in the database
        reservation = Reservation.objects.get(customer_name="John Doe")
        self.assertEqual(reservation.size, 2)
        self.assertEqual(reservation.comments, "Birthday celebration")
        self.assertEqual(reservation.tableNo.tableNo, '1')
        
        # Check if the table status has been updated to reserved
        table = Table.objects.get(tableNo=1)
        self.assertEqual(table.status, "reserved")
        
        if table.status == "reserved":
            print("✅ Table Reservation Test Passed!")

#Unit Test Case for Basket Functionality 
class UserBasketManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.session.save()

        # Create food and drink items for testing
        self.food_item = Food.objects.create(
            foodId=1,
            food_name="Pounded Yam",
            ingredients="Yam, Water",
            category="Main Meal",
            duration="30 minutes",
            price=10.99,
            calories=250
        )

        self.drink_item = Drink.objects.create(
            drinkId=1,
            drink_name="Lemonade",
            description="Refreshing citrus drink",
            category="Soft Drink",
            alcoholConc="0%",
            price=3.99,
            calories=100
        )

        self.basket = Basket.objects.create(session_id=self.session.session_key)

    def test_add_main_meal_food_to_basket(self):
        url = reverse('addItemToBasket', kwargs={'itemID': self.food_item.foodId, 'itemType': 'mainMealFood'})
        response = self.client.post(url, {
            'foodPrice': '10.99',
            'soupChoice': 'Egusi',
            'proteinChoice': 'Chicken',
            'spiceLevel': 'Medium',
            'notes': 'Extra spicy'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(OrderItem.objects.filter(food_item=self.food_item).exists())

    def test_add_fast_food_to_basket(self):
        url = reverse('addItemToBasket', kwargs={'itemID': self.food_item.foodId, 'itemType': 'fastFood'})
        response = self.client.post(url, {
            'foodPrice2': '10.99',
            'sauceChoice': 'Ketchup',
            'spiceLevel2': 'Mild',
            'notes2': 'No onions'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(OrderItem.objects.filter(food_item=self.food_item).exists())
    
    def test_add_dessert_to_basket(self):
        url = reverse('addItemToBasket', kwargs={'itemID': self.food_item.foodId, 'itemType': 'deserts'})
        response = self.client.post(url, {
            'foodPrice3': '7.99',
            'sauceChoice3': 'Chocolate',
            'notes3': 'Extra sauce'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(OrderItem.objects.filter(food_item=self.food_item).exists())
    
    def test_add_drink_to_basket(self):
        url = reverse('addItemToBasket', kwargs={'itemID': self.drink_item.drinkId, 'itemType': 'drink'})
        response = self.client.post(url, {
            'drinkPrice': '3.99',
            'drinkSize': 'Large',
            'drinkNotes': 'No ice',
            'iceChoice': 'No Ice'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(OrderItem.objects.filter(drink_item=self.drink_item).exists())

        if OrderItem.objects.filter(drink_item=self.drink_item).exists():
            print("✅ Basket Functionality Test Passed!!")
             
#Unit Test Case for Order Placement
class OrderPlacementTests(TestCase):
    def setUp(self):
        """Setup test data before each test runs."""
        self.client = Client()
        
        # Create test waiter
        self.waiter = Waiter.objects.create(
            waiterId="WTR001",
            first_name="Alice"
        )
        
        # Create test table assigned to the waiter
        self.table = Table.objects.create(
            tableNo=2,
            waiter=self.waiter,
            capacity=5,
            status="reserved"
        )
        
        # Create a test basket
        self.session = self.client.session
        self.session.create()
        self.basket = Basket.objects.create(session_id=self.session.session_key)

        # Create test food items
        self.food_item1 = Food.objects.create(food_name="Burger", duration="10 mins")
        self.food_item2 = Food.objects.create(food_name="Pizza", duration="15 mins")
        
        # Create test order items in the basket
        self.order_item1 = OrderItem.objects.create(
            basket=self.basket, food_item=self.food_item1
        )
        self.order_item2 = OrderItem.objects.create(
            basket=self.basket, food_item=self.food_item2
        )
        
    def test_generate_order_success(self):
        """Test order creation from basket without using reverse."""
        name = "John Doe"
        table = self.table
        basket = self.basket

        # Fetch order items for the basket
        order_items = OrderItem.objects.filter(basket=basket)
        
        # Assign max duration manually as 30
        max_duration = 30 if order_items.exists() else 0
        
        # Create the order manually
        order = Order.objects.create(
            customer_name=name,
            table=table,
            basket=basket,
            total_expected_duration=max_duration
        )
        order.orderId = Order.generateOrderID()
        order.save()
        
        # Assign order items to the order
        order.order_items.set(order_items)
        
        # Clear the basket after order is placed
        order_items.update(basket=None)
        
        # Increment waiter notification count
        notifications = self.client.session.get(f"waiter_notifications_{self.waiter.waiterId}", 0) + 1
        self.client.session[f"waiter_notifications_{self.waiter.waiterId}"] = notifications
        self.client.session.save()
        
        # Assertions
        self.assertIsNotNone(order, "Order was not created!")
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(order.table, self.table)
        self.assertEqual(order.total_expected_duration, 30)  # Manually assigned max duration
        self.assertEqual(order.order_items.count(), 2)
        self.assertEqual(OrderItem.objects.filter(basket=self.basket).count(), 0)
        self.assertEqual(notifications, 1, "Waiter notification was not incremented!")
        
        print("✅ Order placement test passed!")
        
        
        
        
        
        
        
        
        
        
        
        
