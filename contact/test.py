from django.test import TestCase
from django.urls import reverse
from contact.models import ContactMessage


class ContactModelTests(TestCase):
    """
    Test cases for the ContactMessage model
    """

    def test_contact_message_str_returns_correct_format(self):
        """
        Test that ContactMessage __str__ returns name and email
        """
        message = ContactMessage.objects.create(
            name="John Doe",
            email="john@example.com",
            message="Test message"
        )
        expected_str = "Message from John Doe (john@example.com)"
        self.assertEqual(str(message), expected_str)


class ContactViewTests(TestCase):
    """
    Test cases for the contact views
    """

    def test_contact_view_get(self):
        """
        Test GET request returns contact form page
        """
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_contact_view_post_valid(self):
        """
        Test submitting valid contact form saves message and redirects
        """
        form_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Hello there!',
        }
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertRedirects(response, reverse('message_sent'))

    def test_contact_view_post_invalid(self):
        """
        Test submitting invalid form does not save and returns form page
        """
        form_data = {
            'name': '',
            'email': 'invalidemail',
            'message': '',
        }
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_message_sent_view(self):
        """
        Test that the message_sent view loads correctly
        """
        response = self.client.get(reverse('message_sent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/message_sent.html')
