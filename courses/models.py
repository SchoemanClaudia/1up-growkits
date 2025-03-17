from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail

class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    video_url = models.URLField(help_text="Private video link for enrolled users")
    duration = models.DurationField(help_text="Duration in hours and minutes")
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    access_granted = models.BooleanField(default=False)

    def send_course_email(self):
        """Send course access email to user after payment confirmation"""
        if self.is_paid and not self.access_granted:
            subject = f"Access to {self.course.title}"
            message = (
                f"Hello {self.user.first_name},\n\n"
                f"Thank you for purchasing {self.course.title}!\n"
                f"You can access your course using the link below:\n\n"
                f"{self.course.video_url}\n\n"
                f"Fungi Greetings - 1up GrowKit Team"
            )
            send_mail(
                subject,
                message,
                'noreply@1upgrowkits.com',
                [self.user.email],
                fail_silently=False,
            )
            self.access_granted = True
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({'Paid' if self.is_paid else 'Pending'})"
