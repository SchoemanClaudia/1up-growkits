from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile
from checkout.models import Order


class ProfileModelTests(TestCase):
    """
    Test cases for the UserProfile model
    """

    def test_userprofile_str_returns_username(self):
        """Test that UserProfile __str__ returns the username."""
        user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), 'testuser')


class ProfileViewTests(TestCase):
    """
    Test cases for profile and order history views
    """

    def setUp(self):
        """Create user, profile, and sample order."""
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.profile = UserProfile.objects.get(user=self.user)

        self.order = Order.objects.create(
            full_name="Test User",
            email="test@example.com",
            phone_number="123456789",
            country="IE",
            town_or_city="Dublin",
            street_address1="123 Street",
            postcode="D01",
            original_bag="{}",
            stripe_pid="test_pid",
        )

    def test_profile_view_requires_login(self):
        """
        Test that profile page redirects if user not logged in
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_logged_in(self):
        """
        Test that logged-in user can access profile page
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_order_history_view(self):
        """
        Test that order history page loads correctly
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('order_history', args=[self.order.order_number])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
