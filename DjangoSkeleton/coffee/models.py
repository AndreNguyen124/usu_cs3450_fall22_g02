from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

def get_absolute_url(self):
  return reverse('my_app:my_app', kwargs={'slug': self.slug })


class Inventory_Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"id: {self.id}  |  Name: {self.name}"
