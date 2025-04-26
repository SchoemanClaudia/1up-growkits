from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Enrollment


class CourseModelTests(TestCase):
    """
    Test cases for the Course model
    """

    def test_course_str_returns_title(self):
        """
        Test that the Course __str__ method returns the course title
        """
        course = Course.objects.create(
            title="Beginner's Mushroom Course",
            price=99.99,
            description="Learn how to grow mushrooms.",
            duration="2:00:00",
            attendee_qty=10,
        )
        self.assertEqual(str(course), "Beginner's Mushroom Course")

    def test_spaces_left_calculation(self):
        """
        Test that spaces_left property calculates correctly
        """
        course = Course.objects.create(
            title="Advanced Course",
            price=120.00,
            description="Advanced growing techniques.",
            duration="3:00:00",
            attendee_qty=5,
        )
        user = User.objects.create_user(username="testuser", password="pass")
        Enrollment.objects.create(
            course=course,
            user=user,
            spots_booked=2,
            is_paid=True,
        )
        self.assertEqual(course.spaces_left, 3)


class EnrollmentModelTests(TestCase):
    """
    Test cases for the Enrollment model
    """

    def setUp(self):
        """
        Create a course and user for enrollment testing
        """
        self.user = User.objects.create_user(
            username='student', password='testpass'
        )
        self.course = Course.objects.create(
            title="Test Course",
            price=50.00,
            description="Test course description.",
            duration="1:00:00",
            attendee_qty=10,
        )

    def test_enrollment_str_representation(self):
        """
        Test that Enrollment __str__ returns correct format
        """
        enrollment = Enrollment.objects.create(
            course=self.course,
            user=self.user,
            spots_booked=2,
        )
        expected_str = "student - Test Course (2 spots)"
        self.assertEqual(str(enrollment), expected_str)


class CourseViewsTests(TestCase):
    """
    Test cases for the course views
    """

    def setUp(self):
        """
        Set up a sample course and admin user for views testing
        """
        self.course = Course.objects.create(
            title="Sample Course",
            price=75.00,
            description="Sample course description.",
            duration="2:00:00",
            attendee_qty=8,
        )
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@test.com'
        )

    def test_online_courses_view_status_code(self):
        """
        Test that the online_courses view returns a 200 response
        """
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/courses.html')

    def test_course_detail_view_status_code(self):
        """
        Test that the course_detail view returns a 200 response
        """
        url = reverse('course_detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    def test_add_course_view_redirects_if_not_logged_in(self):
        """
        Test that add_course redirects non-logged users
        """
        url = reverse('add_course')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_add_course_view_for_superuser(self):
        """
        Test that superuser can access add_course view
        """
        self.client.login(username='admin', password='adminpass')
        url = reverse('add_course')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/add_course.html')

    def test_edit_course_view_redirects_if_not_superuser(self):
        """
        Test that edit_course redirects non-superusers
        """
        url = reverse('edit_course', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_course_view_redirects_if_not_superuser(self):
        """
        Test that delete_course redirects non-superusers
        """
        url = reverse('delete_course', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
