from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product


class ProductModelTests(TestCase):
    """
    Test cases for the Product model
    """

    def test_product_str_returns_name(self):
        """
        Test that the Product __str__ method returns the product name
        """
        product = Product.objects.create(
            name="Test Product",
            price=10.00,
            stock_quantity=10,
        )
        self.assertEqual(str(product), "Test Product")

    def test_low_stock_indicator_updates_correctly(self):
        """
        Test that low stock indicator updates based on stock quantity
        """
        product = Product.objects.create(
            name="Low Stock Product",
            price=10.00,
            stock_quantity=2,
        )
        product.save()
        self.assertTrue(product.low_stock_indicator)

        product.stock_quantity = 10
        product.save()
        self.assertFalse(product.low_stock_indicator)


class ProductViewsTests(TestCase):
    """
    Test cases for the product views
    """

    def setUp(self):
        """
        Set up a product and a superuser for testing
        """
        self.product = Product.objects.create(
            name="Test Product",
            price=10.00,
            stock_quantity=10,
            featured=True,
        )
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@test.com'
        )

    def test_mushroom_kits_view(self):
        """
        Test that the mushroom_kits view returns a 200 response
        """
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_view(self):
        """
        Test that the product_detail view returns a 200 response
        """
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_add_product_view_redirects_if_not_logged_in(self):
        """
        Test that add_product redirects non-logged users to login
        """
        url = reverse('add_product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_add_product_view_for_superuser(self):
        """
        Test that a superuser can access the add_product page
        """
        self.client.login(username='admin', password='adminpass')
        url = reverse('add_product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_edit_product_view_redirects_if_not_superuser(self):
        """
        Test that edit_product redirects non-superusers
        """
        url = reverse('edit_product', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_product_view_redirects_if_not_superuser(self):
        """
        Test that delete_product redirects non-superusers
        """
        url = reverse('delete_product', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
