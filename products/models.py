from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    sku = models.CharField(max_length=254, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) #admin only
    low_stock_indicator = models.BooleanField(default=False) #admin only

    def save(self, *args, **kwargs):
        # Automatically set a low stock alert
        self.low_stock_indicator = self.stock_quantity < 5
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
