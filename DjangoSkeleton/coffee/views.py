from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Inventory_Item
from .forms import InventoryForm


def login(request):
	return render(request, 'coffee/login.html')

def userView(request):
    return render(request, 'coffee/userView.html');

def managerView(request):
    return render(request, 'coffee/managerView.html');

def manageEmployees(request):
    return render(request, 'coffee/manageEmployees.html');
	
	
def inventory(request):
    inventory_list = Inventory_Item.objects.order_by('name')
    context = {
            'inventory_list' : inventory_list

            }

    return render(request, 'coffee/inventory.html', context)


def update_inventory(request, pk):
    item = Inventory_Item.objects.get(id=pk)
    if request.method=='POST':
        form = InventoryForm(request.POST, initial={'quantity': 1})
        if form.is_valid():
            howMuch  = form.cleaned_data['quantity']
            form.save(commit=False)

            item.gainInventory(howMuch)

            return redirect('coffee:inventory')

    else:
        form = InventoryForm(initial = {'quantity': 1})
        
    context = {
            'form' : form,
            }
    return render(request, 'coffee/update_inventory.html', context)
	
	
