from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Inventory_Item

# from .models import custom_function


def index(request):
	return render(request, 'coffee/index.html')

def login(request):
	return render(request, 'coffee/login.html')
	
	
def manage_inventory(request):
    inventory_list = Inventory_Item.objects.order_by('name')
    context = {
            'inventory_list' : inventory_list

            }

    return render(request, 'coffee/manage_inventory.html', context)
	
	
