import uuid

from django.db import models
from django.db.models import Sum, Q
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from courses.models import Course, Enrollment
from profiles.models import UserProfile

# Create your models here.


class Order(models.Model):
    PENDING = 'Pending'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    COURSE_BOOKED = 'Course Booked'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (COURSE_BOOKED, 'Course Booked'),
    ]

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING,
    )

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        """
        Update grand total each time a line item is added,
        calculating delivery based only on physical products.
        """
        all_items_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0

        physical_items_total = self.lineitems.filter(product__isnull=False).aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0

        self.order_total = all_items_total

        if 0 < physical_items_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = physical_items_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost

        print(f"All total: {self.order_total} | Physical total: {physical_items_total} | Delivery: {self.delivery_cost}")

        self.save()

    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    
    # Populated depending on item type
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)

    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        if self.product:
            price = self.product.price
        elif self.course:
            price = self.course.price
        else:
            price = 0

        self.lineitem_total = price * self.quantity
        super().save(*args, **kwargs)

        self.order.update_total()

    def __str__(self):
        if self.product:
            return f'SKU {self.product.sku} on order {self.order.order_number}'
        elif self.course:
            return f'Course {self.course.title} on order {self.order.order_number}'
        return f'Item on order {self.order.order_number}'