from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

def get_absolute_url(self):
    return reverse('my_app:my_app', kwargs={'slug': self.slug})


class Inventory_Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def gainInventory(self, value):
        self.quantity += value
        self.save()

    def useInventory(self, value):
        self.quantity -= value
        self.save()

    def __str__(self):
        return f"\n\tid: {self.id} \n\tName: {self.name} \n\tQuantity: {self.quantity} \n\tPrice: {self.price}"


class Drink_Item(models.Model):
    name = models.CharField(max_length=200)

    # TODO: Using a charField need to determine if there is a way to implement a dictionary in the model
    Ingredients = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"\n\tid: {self.id} \n\tName: {self.name} \n\tQuantity: {self.Ingredients} \n\tPrice: {self.price}"


# order_item: composed of many drinks