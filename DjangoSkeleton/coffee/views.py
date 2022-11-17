from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users
from .forms import InventoryForm, CreateUserForm, PriceMarkupForm, AccountBalanceForm, LogHoursForm, DrinkForm, MenuForm
from .models import Inventory_Item, Price_Markup, Profile, Menu_Item, Order, Item_Amount 
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
def shoppingCartView(request):
    current_orderq = Order.objects.filter(profile__id=request.user.id, status=0)
    if current_orderq.exists():
        current_order = current_orderq.first()
        print('current order:', current_order)
        print('current order:', current_order.menu_item_set.all())

        order_total = calculateOrderTotal(current_order.id)
        context = {
                'current_order': current_order,
                'order_total': order_total
                }
    else:
        context = {'current_order': ''}

    if request.method == 'POST':
        total =  Decimal(request.POST.get('checkout'))

        user = Profile.objects.get(id=request.user.id)

        if user.account_balance >= total:
            user.decreaseBalance(total)
            # This should probably be handled in models eventually
            current_order.status=1
            current_order.save()

            return redirect('coffee:login')

        else:
            messages.info(request, 'Error: Insufficient funds')

        print(total)

    return render(request, 'coffee/shopping_cart.html', context)


def calculateOrderTotal(id):
    order = Order.objects.filter(id=id).first()
    menuItems = order.menu_item_set.all()
    total = 0
    for i in menuItems:
        total += i.price

    return total


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Customer', 'Employee'])
# TODO: Need to refactor 'drink_list'
def userView(request):
    drink_list = Menu_Item.objects.filter(custom=False)
    # Menu_Item.objects.order_by('name')
    context = {'drink_list': drink_list}

    return render(request, 'coffee/userView.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Customer', 'Employee'])
def customizeDrink(request, pk):
    ####### Make copy of menuItem ########
    menuItem = Menu_Item.objects.get(id=pk)
    drinkName = 'Custom ' + menuItem.name
    customDrink = Menu_Item(name = drinkName, price = menuItem.price, custom=True)
    customDrink.save()
    for ingr in menuItem.item_amounts.all():    
        Item_Amount.objects.create(menu_item=customDrink, inventory_item=ingr.inventory_item, amount = ingr.amount)
    

    ######## Make various lists for the template context ####### 
    ingred_amounts = customDrink.item_amounts.all()
    ingred_names = [dr.name for dr in customDrink.Ingredients.all()]
    
    ing_amt_dict = {}
    for ingamt in ingred_amounts:
        ing_amt_dict[ingamt.inventory_item.name.split(' ', 1)[0]] = ingamt.amount
    

    ######## Handle POST request and etc ############
    if request.method == 'POST':
        print('submitted!')
       
        custom_ingreds = {
            'caramel' : request.POST.get('caramel'),
            'chai' : request.POST.get('chai'),
            'chocolate' : request.POST.get('chocolate'),
            'cinnamon' : request.POST.get('cinnamon'),
            'espresso' : request.POST.get('espresso'),
            'half' : request.POST.get('half'),
            'ice' : request.POST.get('ice'),
            'irish' : request.POST.get('irish'),
            'matcha' : request.POST.get('matcha'),
            'milk' : request.POST.get('milk'),
            'mocha' : request.POST.get('mocha'),
            'peppermint' : request.POST.get('peppermint'),
            'pumpkin' : request.POST.get('pumpkin'),
            'strawberry' : request.POST.get('strawberry'),
            'vanilla' : request.POST.get('vanilla'),
            'whipped' : request.POST.get('whipped'),
        }

        ########## Customize the drink based on form specifications ##########
        for ing in custom_ingreds:
            amt = int(custom_ingreds[ing])
            if amt > 0:
                inv_item = Inventory_Item.objects.get(name__startswith=ing)
                item_amt, created = Item_Amount.objects.get_or_create(menu_item=customDrink, inventory_item=inv_item)
                item_amt.updateAmount(amt)
                
                
        ######### Handle adding the custom drink to the current order ##########
        whos_ordering = Profile.objects.get(id=request.user.id) #TODO make this adjustable for cashier creating customer order
        print('user ordering is ', whos_ordering)
        orders = Order.objects.filter(profile=whos_ordering, status=0)  
        print('current order is: ', orders)
        if not orders.exists():
            current_order = Order.objects.create(profile=whos_ordering)
        else:
            current_order = orders[0]
        customDrink.order = current_order
        customDrink.save()
        new_price = getMenuItemPrice(customDrink.id)
        customDrink.updatePrice(new_price)
        return redirect('coffee:userView')

    context = { 'drink' : customDrink, 'drinkIngreds' : ingred_names, 'ingredAmounts' : ing_amt_dict}
    return render(request, 'coffee/customizeDrink.html', context)



@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Employee'])
def employeeView(request):
    order_list = Order.objects.filter(status=2)
    context = { 'order_list': order_list }

    if request.method == 'POST':
        try:
            pk = request.POST.get('id')
            order = Order.objects.get(id=pk)
            order.changeStatus(3)
            return render(request, 'coffee/employeeView.html', context)
        except: # If there is an empty post request, do nothing
            None
    return render(request, 'coffee/employeeView.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Employee'])
def deliverDrinks(request):
    order_list = Order.objects.filter(status=3)
    context = { 'order_list': order_list }

    if request.method == 'POST':
        try:
            pk = request.POST.get('id')
            order = Order.objects.get(id=pk)
            order.changeStatus(4)
            return render(request, 'coffee/deliverDrinks.html', context)
        except: # If there is an empty post request, do nothing
            None
    return render(request, 'coffee/deliverDrinks.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager'])
def managerView(request):
    return render(request, 'coffee/managerView.html')


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Employee'])
def manageEmployees(request):
    if 'q' in request.GET:
        q = request.GET['q']
        users = Profile.objects.filter(user__username__icontains=q)

        context = {
            'users': users,
            'clearSearch': True
        }
    else:
        context = {'clearSearch': False}
    return render(request, 'coffee/manageEmployees.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Employee'])
def viewPaidOrders(request, pk):
    userProfile = Profile.objects.get(id=pk)

    context = {
        'customer': userProfile
    }

    return render(request, 'coffee/paidOrders.html', context)


@login_required(login_url='coffee:login')
@allowed_users(allowed_roles=['Manager', 'Employee'])
def viewPaidOrders(request, pk):
    userProfile = Profile.objects.get(id=pk)

    # list orders for given user with a status of 'Paid'
    paidOrders = Order.objects.filter(profile__id=userProfile.id, status=1)

    if request.method == 'POST':
        orderID = request.POST.get('to-barista')
        order = Order.objects.filter(id=orderID).first()    # Have to grab first because filter returns a query set of one

        # this should eventually be handled in models.py
        print("Old order status:")
        print(order.status)
        order.status = 2
        order.save()
        print("New order status:")
        print(order.status)


    context = {
            'customer' : userProfile,
            'paidOrderList' : paidOrders
            }


    return render(request, 'coffee/paidOrders.html', context)


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

    drink_list = Menu_Item.objects.filter(custom=False).order_by('name')
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
            updateAllPrices()

            return redirect('coffee:edit-menu')

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
            menu_item = form.save()
            menu_item.updatePrice(getMenuItemPrice(menu_item.id))
            return redirect('coffee:drink')
    else:
        form = DrinkForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'coffee/drink_update.html', context)


# TODO: Implement Add/Remove/Edit Menu Item
# @login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager'])
def menuItem(request):
    menu_list = Menu_Item.objects.filter(custom=False)
    markup = Price_Markup.objects.first()
    context = {
        'menu_list': menu_list,
        'markup': markup
    }
    return render(request, 'coffee/menuItem.html', context)


# TODO
# addDrinkProduct
# @login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager'])
def addMenuItem(request):
    #item = Menu_Item.objects.get(id=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            #item.save()
            form.save()
            updateAllPrices()
            return redirect('coffee:edit-menu')
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
        return redirect('coffee:edit-menu')
    return render(request, 'coffee/menu_delete.html')


# @login_required(login_url='coffee:login')
# @allowed_users(allowed_roles=['Manager'])
def menu_update(request, pk):
    item = Menu_Item.objects.get(id=pk)

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            item.updatePrice(getMenuItemPrice(item.id))
            return redirect('coffee:edit-menu')
    else:
        form = MenuForm(instance=item)
    context = {
        'form': form

    }
    return render(request, 'coffee/menu_update.html', context)


def getMenuItemPrice(itemId):
    menuItem = Menu_Item.objects.get(id=itemId)
    markupDecimal = (Price_Markup.objects.first().markup / 100) + 1

    price = 2
    for i in menuItem.Ingredients.all():
        price += i.price

    price = price * Decimal(markupDecimal)

    # --- Uncomment when testing is done to add baseline price
    # if price < 7.50: price = 7.50

    return price


def updateAllPrices():
    menuItems = Menu_Item.objects.all()
    for item in menuItems:
        item.updatePrice(getMenuItemPrice(item.id))


def notAuth(request):
    return render(request, 'coffee/notAuth.html')
