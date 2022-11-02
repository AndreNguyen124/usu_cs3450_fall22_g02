from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users

from .models import Inventory_Item, Menu_Item #Drink_Item
from .forms import InventoryForm, CreateUserForm, DrinkForm, MenuForm
from .models import Inventory_Item, Price_Markup, Profile, Menu_Item #Drink_Item
from .forms import InventoryForm, CreateUserForm, PriceMarkupForm, AccountBalanceForm, LogHoursForm, DrinkForm

from decimal import Decimal


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
@allowed_users(allowed_roles=['Manager'])
def createEmployee(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Employee')
            user.groups.add(group)
            user.profile.hours_worked = 0
            user.save()

            messages.success(request, 'Employee account was created successfully')
            return redirect('coffee:managerView')

    context = {'form': form}
    return render(request, 'coffee/createEmployee.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Customer', 'Employee'])
def update_account_balance(request):
    user = Profile.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AccountBalanceForm(request.POST, initial={'account_balance': 1})
        if form.is_valid():
            form.save(commit=False) 
            user.increaseBalance(form.cleaned_data['account_balance'])

            return redirect('coffee:login')

    else:
        form = AccountBalanceForm(initial={'account_balance': 1})

    context = {
        'form': form,
    }
    return render(request, 'coffee/update_account_balance.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Employee'])
def update_hours(request):
    user = Profile.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = LogHoursForm(request.POST, initial={'hours_worked': 1})
        if form.is_valid():
            form.save(commit=False) 
            user.logHours(form.cleaned_data['hours_worked'])

            return redirect('coffee:login')

    else:
        form = LogHoursForm(initial={'hours_worked': 1})

    context = {
        'form': form,
    }
    return render(request, 'coffee/update_hours.html', context)


def getTotalHoursWorked():
    total = 0
    employees = Group.objects.get(id=3).user_set.all()
    for i in employees:
        user = Profile.objects.get(id=i.id)
        total += user.hours_worked

    return total


def clearAllHours():
    employees = Group.objects.get(id=3).user_set.all()
    for i in employees:
        user = Profile.objects.get(id=i.id)
        user.clearHours()


def payAllEmployees():
    employees = Group.objects.get(id=3).user_set.all()
    for i in employees:
        user = Profile.objects.get(id=i.id)
        user.increaseBalance(15 * user.hours_worked)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def payEmployees(request):
    manager = Profile.objects.first()
    totalOwed = 15 * getTotalHoursWorked()

    if manager.account_balance >= totalOwed:
        payAllEmployees()
        clearAllHours()
        manager.decreaseBalance(totalOwed)

    else:
        messages.info(request, 'Error: Insufficient funds')
        return HttpResponseRedirect('/managerView')
        
    return redirect('coffee:managerView')



@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Customer', 'Employee'])
def userView(request):
    drink_list = Menu_Item.objects.order_by('name')
    context = { 'drink_list': drink_list }

    return render(request, 'coffee/userView.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Customer', 'Employee'])
def customizeDrink(request, pk):
    item = Menu_Item.objects.get(id=pk)
    if request.method == 'POST':
        form = DrinkForm(request.POST, instance=item)

    context = {'drink': item}
    return render(request, 'coffee/customizeDrink.html', context)
    

@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Employee'])
def employeeView(request):
    return render(request, 'coffee/employeeView.html')


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def managerView(request):
    return render(request, 'coffee/managerView.html')


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def manageEmployees(request):
    return render(request, 'coffee/manageEmployees.html')


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def inventory(request):
    inventory_list = Inventory_Item.objects.order_by('name')
    context = {
        'inventory_list': inventory_list
    }

    return render(request, 'coffee/inventory.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def update_inventory(request, pk):
    manager = Profile.objects.first()
    item = Inventory_Item.objects.get(id=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, initial={'quantity': 1})
        if form.is_valid():
            manager = Profile.objects.first()
            
            howMuch = form.cleaned_data['quantity']
            totalOwed = item.price * howMuch

            if manager.account_balance >= totalOwed:
                item.gainInventory(howMuch)
                manager.decreaseBalance(totalOwed)
            else:
                messages.info(request, 'Error: Insufficient funds')
                return HttpResponseRedirect('/inventory')


            form.save(commit=False)

            return redirect('coffee:inventory')

    else:
        form = InventoryForm(initial={'quantity': 1})

    context = {
        'form': form,
    }
    return render(request, 'coffee/update_inventory.html', context)

def product_delete(request, pk):
    item = Menu_Item.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('coffee:drink')
    return render(request, 'coffee/drink_delete.html')

def drink(request):
    return render(request, 'coffee/drink.html')


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def drinkProduct(request):
    markup = Price_Markup.objects.first()

    drink_list = Menu_Item.objects.order_by('name')
    context = {
        'drink_list': drink_list,
            'markup': markup
    }

    return render(request, 'coffee/drink.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def update_markup(request):
    markupObj = Price_Markup.objects.first()
    if request.method == 'POST':
        form = PriceMarkupForm(request.POST, initial={'markup': markupObj.markup})
        if form.is_valid():
            form.save(commit=False)
            markupObj.setPriceMarkup(form.cleaned_data['markup'])

            return redirect('coffee:drink')

    else:
        form = PriceMarkupForm(initial={'markup': markupObj.markup})

    context = {
        'form': form,
    }
    return render(request, 'coffee/update_markup.html', context)

@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def addDrinkProduct(request, pk):
    item = Menu_Item.objects.get(id=pk)
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


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def product_delete(request, pk):
    item = Menu_Item.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('coffee:drink')
    return render(request, 'coffee/drink_delete.html')

@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def product_update(request, pk):
    item = Menu_Item.objects.get(id=pk)

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


# TODO: Implement Add/Remove/Edit Menu Item
@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def menuItem(request):
    menu_list = Menu_Item.objects.all()
    context = {
        'menu_list': menu_list
    }
    return render(request, 'coffee/menuItem.html', context)

# TODO
# addDrinkProduct
@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def addMenuItem(request, pk):
    item = Menu_Item.objects.get(id=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            item.save()
            form.save()
            return redirect('coffee:menu')
    else:
        form = MenuForm()

    context = {
        'form': form,
    }
    return render(request, 'coffee/menu_add.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def deleteMenuItem(request, pk):
    item = Menu_Item.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('coffee:menu')
    return render(request, 'coffee/menu_delete.html')



@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def menu_update(request, pk):
    item = Menu_Item.objects.get(id=pk)

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return redirect('coffee:menu')
    else:
        form = MenuForm(instance=item)
    context = {
        'form': form

    }
    return render(request, 'coffee/menu_update.html', context)


def getMenuItemPrice(itemId):
    menuItem = Menu_Item.objects.get(id=itemId)
    markupDecimal = (Price_Markup.objects.first().markup / 100) + 1

    price = 0
    for i in menuItem.Ingredients.all():
        price += i.price

    price = price * Decimal(markupDecimal)

    if price < 7.50: return 7.50

    return price

