from django.contrib import admin

# Register your models here.
from .models import Inventory_Item, Menu_Item
from .models import Inventory_Item, Price_Markup, Profile
from .models import Drink_Item

admin.site.register(Inventory_Item)
admin.site.register(Menu_Item)
admin.site.register(Drink_Item)
admin.site.register(Price_Markup)

