from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users

from .models import Inventory_Item, Drink_Item
from .forms import InventoryForm, CreateUserForm, DrinkForm


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'Customer':
                    return redirect('coffee:userView')
                elif group == 'Employee':
                    return redirect('coffee:employeeView')
                else:
                    return redirect('coffee:managerView')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'coffee/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('coffee:login')


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)

            messages.success(request, 'Account was created successfully')
            return redirect('coffee:login')

    context = {'form': form}
    return render(request, 'coffee/register.html', context)


@login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager', 'Customer', 'Employee'])
def userView(request):
    return render(request, 'coffee/userView.html')


@login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager', 'Employee'])
def employeeView(request):
    return render(request, 'coffee/employeeView.html')


@login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager'])
def managerView(request):
    return render(request, 'coffee/managerView.html')


@login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager'])
def manageEmployees(request):
    return render(request, 'coffee/manageEmployees.html')


@login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager'])
def inventory(request):
    inventory_list = Inventory_Item.objects.order_by('name')
    context = {
        'inventory_list': inventory_list
    }

    return render(request, 'coffee/inventory.html', context)


@login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager'])
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


def drink(request):
    return render(request, 'coffee/drink.html')


def drinkProduct(request):
    drink_list = Drink_Item.objects.order_by('name')
    context = {
        'drink_list': drink_list
    }

    return render(request, 'coffee/drink.html', context)


def addDrinkProduct(request, pk):
    item = Drink_Item.objects.get(id=pk)
    if request.method == 'POST':
        form = DrinkForm(request.POST)
        if form.is_valid():
            item.save()
            form.save()
            return redirect('coffee:drink')
    else:
        form = DrinkForm()

    context = {
        'form': form,
    }
    return render(request, 'coffee/drink_add.html', context)


def product_delete(request, pk):
    item = Drink_Item.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('coffee:drink')
    return render(request, 'coffee/drink_delete.html')


def product_update(request, pk):
    item = Drink_Item.objects.get(id=pk)

    if request.method == 'POST':
        form = DrinkForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return redirect('coffee:drink')
    else:
        form = DrinkForm(instance=item)
    context = {
        'form': form

    }
    return render(request, 'coffee/drink_update.html', context)
