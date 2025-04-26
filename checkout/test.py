from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from checkout.models import Order, OrderLineItem
from products.models import Product
from courses.models import Course
from profiles.models import UserProfile


class CheckoutModelTests(TestCase):
    """
    Test cases for Order and OrderLineItem models
    """

    def setUp(self):
        """
        Create test data for checkout models
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.profile = UserProfile.objects.get(user=self.user)

        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal('10.00'),
            stock_quantity=10,
            description="Sample product",
        )

        self.course = Course.objects.create(
            title="Test Course",
            price=Decimal('50.00'),
            description="Sample course",
            duration="2:00:00",
            attendee_qty=5,
        )

        self.order = Order.objects.create(
            full_name="Test User",
            email="test@example.com",
            phone_number="123456789",
            country="IE",
            town_or_city="Dublin",
            street_address1="123 Street",
            postcode="D01",
            delivery_cost=Decimal('5.00'),
            order_total=Decimal('60.00'),
            grand_total=Decimal('65.00'),
            original_bag="{}",
            stripe_pid="test_pid",
            user_profile=self.profile,
        )

    def test_order_str_returns_order_number(self):
        """
        Test that the Order __str__ method returns order number
        """
        self.assertEqual(str(self.order), self.order.order_number)

    def test_orderlineitem_str_returns_correct_string(self):
        """
        Test OrderLineItem string representation for product and course
        """
        product_lineitem = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        expected_product_str = (
            f'SKU {self.product.sku} on order {self.order.order_number}'
        )
        self.assertEqual(str(product_lineitem), expected_product_str)

        course_lineitem = OrderLineItem.objects.create(
            order=self.order,
            course=self.course,
            quantity=1
        )
        expected_course_str = (
            f'Course {self.course.title} on order {self.order.order_number}'
        )
        self.assertEqual(str(course_lineitem), expected_course_str)

    def test_order_total_calculation(self):
        """
        Test that order total updates correctly after adding lineitems
        """
        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3
        )
        self.order.refresh_from_db()

        expected_order_total = self.product.price * 3
        expected_physical_total = expected_order_total

        # If physical total is under free delivery threshold = delivery applies
        free_delivery_threshold = Decimal('50.00')
        standard_delivery_percentage = Decimal('10.00')  # 10%

        if 0 < expected_physical_total < free_delivery_threshold:
            delivery_percentage = standard_delivery_percentage / Decimal('100')
            expected_delivery = expected_physical_total * delivery_percentage
        else:
            expected_delivery = Decimal('0.00')

        expected_grand_total = expected_order_total + expected_delivery

        self.assertEqual(self.order.order_total, expected_order_total)
        self.assertEqual(self.order.delivery_cost, expected_delivery)
        self.assertEqual(self.order.grand_total, expected_grand_total)
