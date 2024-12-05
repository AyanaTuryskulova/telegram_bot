from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    descripption = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
