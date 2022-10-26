from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

def get_absolute_url(self):
    return reverse('my_app:my_app', kwargs={'slug': self.slug})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=7, default=0.00, decimal_places=2) # null and blank let hours be an optional field (only employees)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    # orders will be associated by having 
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    # in their class definition (this creates the many to one relationship)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        newUser = instance
        if created:
            Profile.objects.create(user=newUser)
            
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    
    def increaseBalance(self, amount):
        self.account_balance += amount
        self.save()

    def decreaseBalance(self, amount):
        self.account_balance -= amount
        self.save()

    def logHours(self, amount):
        self.hours_worked += amount
        self.save()

    def clearHours(self):
        self.hours_worked = 0
        self.save()


    def __str__(self):
        return f"\n\tUser: {self.user}"


class Price_Markup(models.Model):
    markup = models.IntegerField(default=0)

    def setPriceMarkup(self, newValue):
        self.markup = newValue
        self.save()

    def __str__(self):
        return f"\n\tid: {self.id} \n\tMarkup: {self.markup}"


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


#class Order_Item:(models.Model):
#    customerName = models.CharField(max_length=200)


