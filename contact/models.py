from django.db import models


class ContactMessage(models.Model):
    """
    Store messages submitted via contact form.
    Includes sender name, email, message content and time sent.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
