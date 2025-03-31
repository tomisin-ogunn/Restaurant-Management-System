from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password
from users.models import Manager, Waiter, Customer
from django.urls import reverse

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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
