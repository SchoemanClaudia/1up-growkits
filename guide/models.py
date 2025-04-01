from django.db import models

# Create your models here.


class GrowGuide(models.Model):
    guide_title = models.CharField(max_length=100)
    instructions = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.guide_title
