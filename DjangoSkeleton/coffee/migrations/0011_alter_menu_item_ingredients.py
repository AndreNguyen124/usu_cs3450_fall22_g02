# Generated by Django 4.1.2 on 2022-11-05 19:43

from django.db import migrations, models
from coffee.views import getMenuItemPrice
from django.contrib.auth.models import Group, User

def populate_db(apps, schema):
    manager_group, createdm = Group.objects.get_or_create(name='Manager')
    customer_group, createdc = Group.objects.get_or_create(name='Customer')
    employee_group, createde = Group.objects.get_or_create(name='Employee')

    manager = User.objects.create_user(username='managerDan', password='imtheboss')
    manager.save()
    manager.groups.add(manager_group)

    employee = User.objects.create_user(username='workerJill', password='ilovetowork')
    employee.save()
    employee.groups.add(employee_group)
    employee.profile.hours_worked = 0.0
    employee.save()
    
    customer = User.objects.create_user(username='personJoe', password='goodpassword')
    customer.save()
    customer.groups.add(customer_group)


    Price_Markup = apps.get_model('coffee', 'Price_Markup')
    Price_Markup.objects.all().delete()

    markup = Price_Markup(markup=43)
    markup.save()

    Menu_Item = apps.get_model('coffee', 'Menu_Item')
    Menu_Item.objects.all().delete()
    Inventory_Item = apps.get_model('coffee', 'Inventory_Item')
    Inventory_Item.objects.all().delete()

    i1 = Inventory_Item(name='Milk', quantity=4, price=0.35)
    i1.save()

    i2 = Inventory_Item(name='Ice', quantity=20, price=0.20)
    i2.save()

    i3 = Inventory_Item(name='Vanilla Base', quantity=15, price=1.05)
    i3.save()

    i4 = Inventory_Item(name='Mocha Base', quantity=15, price=1.20)
    i4.save()

    i5 = Inventory_Item(name='Caramel Base', quantity=20, price=1.05)
    i5.save()

    i6 = Inventory_Item(name='Pumpkin Spice Syrup', quantity=10, price=0.50)
    i6.save()

    i7 = Inventory_Item(name='Chocolate Chips', quantity=30, price=0.45)
    i7.save()

    i8 = Inventory_Item(name='Whipped Cream', quantity=20, price=1.00)
    i8.save()

    i9 = Inventory_Item(name='Matcha Powder', quantity=7, price=0.85)
    i9.save()

    i10 = Inventory_Item(name='Cup', quantity=50, price=0.60)
    i10.save()

    i11 = Inventory_Item(name='Strawberry Puree', quantity=30, price=1.20)
    i11.save()

    i12 = Inventory_Item(name='Lids', quantity=50, price=0.50)
    i12.save()

    i13 = Inventory_Item(name='Irish Cream Syrup', quantity=20, price=0.50)
    i13.save()

    i14 = Inventory_Item(name='Half and Half', quantity=20, price=0.40)
    i14.save()

    i15 = Inventory_Item(name='Espresso Shot', quantity=20, price=0.20)
    i15.save()

    i16 = Inventory_Item(name='Chai Tea Base', quantity=50, price=0.60)
    i16.save()

    i17 = Inventory_Item(name='Cinnamon', quantity=50, price=0.10)
    i17.save()

    i18 = Inventory_Item(name='Peppermint', quantity=50, price=0.10)
    i18.save()

    m1 = Menu_Item(name='Caramel Frap')
    m1.save()
    m1.price = getMenuItemPrice(m1.id)
    m1.save()
    # m1.Ingredients.add(i1, i2, i5, i12, i10)
    # m1.save()
    

    # m2 = Menu_Item(name='Mocha Frap')
    # m2.save()
    # m2.Ingredients.add(i1, i2, i4, i8, i12, i10)
    # m2.save()
    # m2.price = getMenuItemPrice(m2.id)
    # m2.save()


    # m3 = Menu_Item(name='Pink Lady')
    # m3.save()
    # m3.Ingredients.add(i1, i2, i3, i10, i11, i12)
    # m3.save()
    # m3.price = getMenuItemPrice(m3.id)
    # m3.save()

    # m4 = Menu_Item(name='Gaelic Storm', price=7.00)
    # m4.save()
    # m4.Ingredients.add(i13, i13, i14, i14, i15, i10)
    # m4.save()

    # m5 = Menu_Item(name='Headless Horseman', price=7.00)
    # m5.save()
    # m5.Ingredients.add(i6, i17, i8, i14, i15, i10)
    # m5.save()

    # m6 = Menu_Item(name='TripleX', price=6.50)
    # m6.save()
    # m6.Ingredients.add(i15, i15, i15, i14, i3, i10)
    # m6.save()

    # m7 = Menu_Item(name='Vanilla Ice', price=6.50)
    # m7.save()
    # m7.Ingredients.add(i3, i3, i15, i14, i2, i10)
    # m7.save()

    # m8 = Menu_Item(name='Chai Lee Latte', price=7.50)
    # m8.save()
    # m8.Ingredients.add(i16, i1, i17, i14, i8, i10)
    # m8.save()

    # m9 = Menu_Item(name='Cocoa Mudslide', price=7.50)
    # m9.save()
    # m9.Ingredients.add(i15, i4, i7, i14, i8, i10)
    # m9.save()

    # m10 = Menu_Item(name='Tis the Season', price=5.50)
    # m10.save()
    # m10.Ingredients.add(i17, i4, i6, i15, i18, i10)
    # m10.save()

class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0010_alter_menu_item_ingredients_item_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_item',
            name='Ingredients',
            field=models.ManyToManyField(blank=True, related_name='inventory_items', through='coffee.Item_Amount', to='coffee.inventory_item'),
        ),
        migrations.RunPython(populate_db)
    ]
