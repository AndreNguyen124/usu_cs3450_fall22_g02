from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Inventory_Item
from .forms import InventoryForm, CreateUserForm


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('coffee:userView')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('coffee:userView')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'coffee/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('coffee:login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('coffee:userView')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Account was created successfully')

                return redirect('coffee:login')

        context = {'form': form}
        return render(request, 'coffee/register.html', context)


@login_required(login_url='coffee:login')
def userView(request):
    return render(request, 'coffee/userView.html')


@login_required(login_url='coffee:login')
def managerView(request):
    return render(request, 'coffee/managerView.html');


@login_required(login_url='coffee:login')
def manageEmployees(request):
    return render(request, 'coffee/manageEmployees.html');


@login_required(login_url='coffee:login')
def inventory(request):
    inventory_list = Inventory_Item.objects.order_by('name')
    context = {
        'inventory_list': inventory_list

    }

    return render(request, 'coffee/inventory.html', context)


@login_required(login_url='coffee:login')
def update_inventory(request, pk):
    item = Inventory_Item.objects.get(id=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, initial={'quantity': 1})
        if form.is_valid():
            howMuch = form.cleaned_data['quantity']
            form.save(commit=False)

            item.gainInventory(howMuch)

            return redirect('coffee:inventory')

    else:
        form = InventoryForm(initial={'quantity': 1})

    context = {
        'form': form,
    }
    return render(request, 'coffee/update_inventory.html', context)


# @login_required(login_url='coffee:login')
def editMenu(request):
    return render(request, 'coffee/editMenu.html')

def addDrinkItem(request):
    return render(request, 'coffee/addDrinkItem.html')

# TODO: Work with Emily
def add(request):
    return None


# TODO: Work With Emily
def addrecord():
    return None


def delete(request, id):
    drink = Inventory_Item.objects.get(id=id)
    drink.delete()
    return HttpResponseRedirect(reverse('index'))


