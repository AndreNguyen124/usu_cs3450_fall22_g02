from django.shortcuts import render
from .models import Inventory_Item
# Create your views here.

def manage_inventory(request):
    inventory_list = Inventory_Item.objects.order_by('name')
    context = {
            'inventory_list' : inventory_list

            }

    return render(request, 'dans_cool_beans/manage_inventory.html', context)
