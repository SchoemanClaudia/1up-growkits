from django.test import TestCase
from django.urls import reverse
from products.models import Product


class HomeViewTests(TestCase):
    """
    Test cases for the home app's index view
    """

    def setUp(self):
        """
        Create sample products for testing
        """
        Product.objects.create(
            name="Featured Product 1",
            price=10.00,
            featured=True,
        )
        Product.objects.create(
            name="Featured Product 2",
            price=20.00,
            featured=True,
        )
        Product.objects.create(
            name="Regular Product",
            price=15.00,
            featured=False,
        )

    def test_index_view_status_code(self):
        """
        Test that the index view returns a 200 OK response
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        """
        Test that the index view uses the correct template
        """
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/index.html')

    def test_index_view_context_featured_products(self):
        """
        Test that the index view passes only featured products in context
        """
        response = self.client.get(reverse('home'))
        featured_products = response.context['featured_products']
        self.assertEqual(len(featured_products), 2)
        self.assertTrue(all(product.featured for product in featured_products))
