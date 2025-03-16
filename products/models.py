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
    stock_quantity = models.IntegerField(default=0)  #track stock levels
    created_at = models.DateTimeField(auto_now_add=True)  #admin only
    low_stock_indicator = models.BooleanField(default=False)  #admin only

    def save(self, *args, **kwargs):
        """ Auto-update a low stock flag to user """
        if self.stock_quantity == 0:
            self.low_stock_indicator = True  #mark if out of stock
        elif self.stock_quantity < 5:
            self.low_stock_indicator = True  #low stock warning
        else:
            self.low_stock_indicator = False  #fully stock
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

