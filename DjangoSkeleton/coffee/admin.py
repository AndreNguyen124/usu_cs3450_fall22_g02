from django.contrib import admin

# Register your models here.
from .models import Inventory_Item, Menu_Item
from .models import Drink_Item

admin.site.register(Inventory_Item)
admin.site.register(Menu_Item)
admin.site.register(Drink_Item)

