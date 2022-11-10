from django.contrib import admin

# Register your models here.
from .models import Inventory_Item, Price_Markup, Profile, Item_Amount, Menu_Item, Order
#from .models import Drink_Item

admin.site.register(Inventory_Item)
admin.site.register(Menu_Item)
#admin.site.register(Drink_Item)
admin.site.register(Price_Markup)
admin.site.register(Profile)
admin.site.register(Item_Amount)
admin.site.register(Order)

