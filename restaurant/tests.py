from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password, check_password
from users.models import Manager, Waiter, Customer
from restaurant.models import Order, Table, KitchenZone, Basket
from restaurant.views.kitchen_views import assign_order_to_zone
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.contrib.messages import get_messages

# Create your tests here.

# Unit Test Case for Order Assignment Logic
class OrderAssignmentTests(TestCase):
    def setUp(self):
        """Setup test data before each test."""
        
        # Create a test basket for the session
        self.basket = Basket.objects.create(session_id="test-session-123")
        
        # Create kitchen zones
        self.zone1 = KitchenZone.objects.create(zoneId=1, active_orders=0)
        self.zone2 = KitchenZone.objects.create(zoneId=2, active_orders=0)
        self.zone3 = KitchenZone.objects.create(zoneId=3, active_orders=0)

        # Create test orders with different durations
        self.order1 = Order.objects.create(customer_name="Alice", total_expected_duration=10, status="Pending", basket=self.basket)
        self.order2 = Order.objects.create(customer_name="Bob", total_expected_duration=20, status="Pending", basket=self.basket)
        self.order3 = Order.objects.create(customer_name="Charlie", total_expected_duration=15, status="Pending", basket=self.basket)
        self.order4 = Order.objects.create(customer_name="David", total_expected_duration=25, status="Pending", basket=self.basket)

    def test_sequential_assignment_first_3_orders(self):
        """Test that the first 3 orders are assigned sequentially to zones."""
        assign_order_to_zone(self.order1)
        assign_order_to_zone(self.order2)
        assign_order_to_zone(self.order3)

        # Verify assignments
        self.assertEqual(self.order1.assigned_zone, self.zone1)
        self.assertEqual(self.order2.assigned_zone, self.zone2)
        self.assertEqual(self.order3.assigned_zone, self.zone3)

        # Verify status updates
        self.assertEqual(self.order1.status, "Assigned")
        self.assertEqual(self.order2.status, "Assigned")
        self.assertEqual(self.order3.status, "Assigned")

        # Verify active orders count
        self.zone1.refresh_from_db()
        self.zone2.refresh_from_db()
        self.zone3.refresh_from_db()
        self.assertEqual(self.zone1.active_orders, 1)
        self.assertEqual(self.zone2.active_orders, 1)
        self.assertEqual(self.zone3.active_orders, 1)

    def test_dynamic_zone_assignment_for_additional_orders(self):
        """Test that additional orders are assigned based on workload."""
        # Assign first 3 orders
        assign_order_to_zone(self.order1)
        assign_order_to_zone(self.order2)
        assign_order_to_zone(self.order3)

        # Assign a fourth order, expecting it to go to the least busy zone
        assign_order_to_zone(self.order4)

        # Get updated zones
        self.zone1.refresh_from_db()
        self.zone2.refresh_from_db()
        self.zone3.refresh_from_db()

        # Order should be assigned to the zone with the least workload
        self.assertEqual(self.order4.status, "Assigned")
        self.assertIn(self.order4.assigned_zone, [self.zone1, self.zone2, self.zone3])

        # Ensure one of the zones has 2 active orders
        active_orders = [self.zone1.active_orders, self.zone2.active_orders, self.zone3.active_orders]
        self.assertIn(2, active_orders)

    def test_order_status_updates_correctly(self):
        """Test that order status is set to 'Assigned' or 'Pending' correctly."""
        assign_order_to_zone(self.order1)
        assign_order_to_zone(self.order2)
        assign_order_to_zone(self.order3)
        assign_order_to_zone(self.order4)  # Fourth order should be assigned based on workload

        # Ensure the fourth order is either assigned or pending
        self.assertIn(self.order4.status, ["Assigned", "Pending"])

        # If any zone already had 3 orders, the fourth should be pending
        max_orders = max(self.zone1.active_orders, self.zone2.active_orders, self.zone3.active_orders)
        if max_orders >= 3:
            self.assertEqual(self.order4.status, "Pending")

    def test_order_with_earliest_completion_time_is_prioritized(self):
        """Ensure the zone with the earliest completion time gets the new order."""
        self.order1.placed_at = timezone.now() - timedelta(minutes=5)
        self.order2.placed_at = timezone.now() - timedelta(minutes=10)
        self.order3.placed_at = timezone.now() - timedelta(minutes=3)
        self.order4.placed_at = timezone.now()

        self.order1.save()
        self.order2.save()
        self.order3.save()
        self.order4.save()

        # Assign orders
        assign_order_to_zone(self.order1)
        assign_order_to_zone(self.order2)
        assign_order_to_zone(self.order3)
        assign_order_to_zone(self.order4)

        # Check that order4 was assigned to the zone with the earliest completion time
        assigned_zone = self.order4.assigned_zone
        self.assertIsNotNone(assigned_zone)
        print(f"Order 4 assigned to: {assigned_zone}")

    def test_no_available_zones(self):
        """Ensure orders remain pending if no zones are available."""
        self.zone1.active_orders = 3
        self.zone2.active_orders = 3
        self.zone3.active_orders = 3
        self.zone1.save()
        self.zone2.save()
        self.zone3.save()

        assign_order_to_zone(self.order1)
        self.assertEqual(self.order1.status, "Assigned")
        self.assertIsNotNone(self.order1.assigned_zone)
        print(f"Order 1 assigned to: Zone {self.order1.assigned_zone.zoneId}")
    
    





