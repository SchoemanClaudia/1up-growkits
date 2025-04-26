from django.test import TestCase
from django.urls import reverse
from .models import GrowGuide


class GrowGuideModelTests(TestCase):
    """
    Test cases for the GrowGuide model
    """

    def test_grow_guide_str_returns_title(self):
        """
        Test that the GrowGuide __str__ method returns the guide title
        """
        guide = GrowGuide.objects.create(
            guide_title="Step 1: Preparation",
            step_no=1,
            instructions="Prepare your kit.",
        )
        self.assertEqual(str(guide), "Step 1: Preparation")

    def test_grow_guide_default_ordering(self):
        """
        Test that GrowGuide objects are ordered by step number
        """
        step1 = GrowGuide.objects.create(
            guide_title="Step 1",
            step_no=1,
            instructions="First step.",
        )
        step2 = GrowGuide.objects.create(
            guide_title="Step 2",
            step_no=2,
            instructions="Second step.",
        )
        guide_steps = GrowGuide.objects.all()
        self.assertEqual(list(guide_steps), [step1, step2])


class GrowGuideViewTests(TestCase):
    """
    Test cases for the grow guide view
    """

    def setUp(self):
        """
        Create some guide steps for testing
        """
        GrowGuide.objects.create(
            guide_title="Step 1",
            step_no=1,
            instructions="First step.",
        )
        GrowGuide.objects.create(
            guide_title="Step 2",
            step_no=2,
            instructions="Second step.",
        )

    def test_grow_guide_view_status_code(self):
        """
        Test that the grow_guide view returns a 200 response
        """
        response = self.client.get(reverse('grow_guide'))
        self.assertEqual(response.status_code, 200)

    def test_grow_guide_view_uses_correct_template(self):
        """
        Test that the grow_guide view uses the correct template
        """
        response = self.client.get(reverse('grow_guide'))
        self.assertTemplateUsed(response, 'guide/grow_guide.html')

    def test_grow_guide_view_context(self):
        """
        Test that the grow_guide view passes all guide steps
        """
        response = self.client.get(reverse('grow_guide'))
        guide = response.context['guide']
        self.assertEqual(len(guide), 2)
