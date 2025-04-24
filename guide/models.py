from django.db import models


class GrowGuide(models.Model):
    """
    A step-by-step instructional guide for growing mushroom kits.
    Each step includes a title, instruction text, optional image,
    and an order number for sequencing in admin.
    """
    guide_title = models.CharField(max_length=100)
    step_no = models.IntegerField(default=0)
    instructions = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.guide_title

    # Order based on set priority
    class Meta:
        ordering = ['step_no']
