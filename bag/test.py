from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from courses.models import Course


class BagViewTests(TestCase):
    """
    Test cases for the bag views
    """

    def setUp(self):
        """
        Create a sample product, course, and user
        """
        self.product = Product.objects.create(
            name="Test Product",
            price=10.00,
            stock_quantity=5,
            description="Sample product",
        )
        self.course = Course.objects.create(
            title="Test Course",
            price=50.00,
            description="Sample course",
            duration="2:00:00",
            attendee_qty=5,
        )
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def test_view_bag_status_code(self):
        """
        Test that view_bag returns a 200 response
        """
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_product_to_bag(self):
        """
        Test adding a product to the bag
        """
        url = reverse('add_to_bag', args=[self.product.id])
        response = self.client.post(url, {
            'quantity': 2,
            'redirect_url': reverse('products'),
            'item_type': 'product',
        })
        bag = self.client.session.get('bag', {})
        self.assertIn(f'product_{self.product.id}', bag)
        self.assertEqual(bag[f'product_{self.product.id}'], 2)
        self.assertEqual(response.status_code, 302)

    def test_add_course_to_bag(self):
        """
        Test adding a course to the bag
        """
        url = reverse('add_to_bag', args=[self.course.id])
        response = self.client.post(url, {
            'quantity': 1,
            'redirect_url': reverse('courses'),
            'item_type': 'course',
        })
        bag = self.client.session.get('bag', {})
        self.assertIn(f'course_{self.course.id}', bag)
        self.assertEqual(bag[f'course_{self.course.id}'], 1)
        self.assertEqual(response.status_code, 302)

    def test_adjust_product_quantity_in_bag(self):
        """
        Test adjusting product quantity in the bag
        """
        session = self.client.session
        session['bag'] = {f'product_{self.product.id}': 1}
        session.save()

        url = reverse('adjust_bag', args=[self.product.id])
        response = self.client.post(url, {
            'quantity': 3,
            'redirect_url': reverse('products'),
            'item_type': 'product',
        })
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[f'product_{self.product.id}'], 3)
        self.assertEqual(response.status_code, 302)

    def test_adjust_course_quantity_in_bag(self):
        """
        Test adjusting course quantity in the bag
        """
        session = self.client.session
        session['bag'] = {f'course_{self.course.id}': 1}
        session.save()

        url = reverse('adjust_bag', args=[self.course.id])
        response = self.client.post(url, {
            'quantity': 2,
            'redirect_url': reverse('courses'),
            'item_type': 'course',
        })
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[f'course_{self.course.id}'], 2)
        self.assertEqual(response.status_code, 302)

    def test_remove_item_from_bag(self):
        """
        Test removing an item from the bag by setting quantity to 0
        """
        session = self.client.session
        session['bag'] = {f'product_{self.product.id}': 1}
        session.save()

        url = reverse('adjust_bag', args=[self.product.id])
        response = self.client.post(url, {
            'quantity': 0,
            'redirect_url': reverse('products'),
            'item_type': 'product',
        })
        bag = self.client.session.get('bag', {})
        self.assertNotIn(f'product_{self.product.id}', bag)
        self.assertEqual(response.status_code, 302)
