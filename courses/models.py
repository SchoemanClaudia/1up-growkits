from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    code = models.CharField(max_length=254, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    start_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date and time the course starts"
    )
    location = models.CharField(
        max_length=255,
        help_text="Physical location of the course",
        null=True,
        blank=True
    )
    duration = models.DurationField(
        help_text="Duration in hours and minutes"
    )
    image = models.ImageField(
        upload_to='course_images/',
        null=True,
        blank=True
    )
    attendee_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def spaces_left(self):
        """
        Return number of available spots based on paid enrollments.
        Only enrollments marked as paid reduce availability.
        """
        valid_enrollments = self.enrollments.filter(is_paid=True)
        total_enrolled = sum(e.spots_booked for e in valid_enrollments)
        return max(0, self.attendee_qty - total_enrolled)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    PENDING = 'Pending'
    ENROLLED = 'Enrolled'
    COMPLETED = 'Completed'

    ENROLLMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ENROLLED, 'Enrolled'),
        (COMPLETED, 'Completed'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spots_booked = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(
        'checkout.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default=PENDING,
    )

    def send_course_email(self):
        """
        Send course details via email to user after payment confirmation.
        Only send email if enrollment is paid and not yet confirmed.
        """
        if self.is_paid and not self.confirmed:
            subject = f"Access to {self.course.title}"
            message = (
                f"Hello There Fungi Fan,\n\n"
                f"Thank you for registering for our {self.course.title}!\n"
                f"Your course details summary:\n\n"
                f"Start Date - {self.course.start_datetime}\n\n"
                f"Location - {self.course.location}\n\n"
                f"Duration - {self.course.duration}\n\n"
                f"Please confirm your attendance by email to "
                f"courses@1up-growkits.com\n\n"
                f"Fungi Greetings - 1up GrowKit Team"
            )
            send_mail(
                subject,
                message,
                'noreply@1up-growkits.com',
                [self.user.email],
                fail_silently=False,
            )

    def __str__(self):
        return (
            f"{self.user.username} - {self.course.title} "
            f"({self.spots_booked} spot{'s' if self.spots_booked > 1 else ''})"
        )
