from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.

def get_absolute_url(self):
    return reverse('my_app:my_app', kwargs={'slug': self.slug})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=7, default=0.00, decimal_places=2) 
    hours_worked = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

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

    def hasPaidOrders(self):
        if Order.objects.filter(profile__id=self.id, status=1):
            print("self has paid orders")
            return True
        else: 
            print("self does not have paid orders")
            return False

    def __str__(self):
        return f"\n\tUser: {self.user}"

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    totalPrice = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    status = models.IntegerField(default=0)
    # 0 : order being created by customer
    # 1 : online order has been paid for - shows up in cashier queue
    # 2 : order submitted to barista to be made - shows in cashier queue
    # 3 : order completed by barista, ready to be delivered to customer - shows in other cashier queue?
    # 4 : delivered to customer - can be deleted

    def changeStatus(self, newStatus):
        self.status = newStatus
        self.save()

    def __str__(self):
        return f"\n\t {self.profile}'s order"



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


class Menu_Item(models.Model):
    name = models.CharField(max_length=200)
    Ingredients = models.ManyToManyField(Inventory_Item, through='Item_Amount', related_name='inventory_items', blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True) 
    custom = models.BooleanField(default = False) # display menu items whose custom=False

    def updatePrice(self, value):
        self.price = value
        self.save()

    def __str__(self):
        return f"\n\tName: {self.name}, \n\tPrice: {self.price}"

class Item_Amount(models.Model):
    inventory_item = models.ForeignKey(Inventory_Item, related_name = 'item_amounts', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu_Item, related_name = 'item_amounts', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"\n\t {self.amount} {self.inventory_item.name}"

    def updateAmount(self, value):
        self.amount = value
        self.save()

# # TODO: Implement a Many to Many Field for Drink Item
# class Drink_Item(models.Model):
#     name = models.CharField(max_length=200)
#     # TODO: Using a charField need to determine if there is a way to implement a dictionary in the model
#     Ingredients = models.CharField(max_length=1000)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f"\n\tid: {self.id} \n\tName: {self.name} \n\tIngredients: {self.Ingredients} \n\tPrice: {self.price}"

