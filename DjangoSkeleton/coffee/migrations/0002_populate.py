# Generated by Django 4.1.2 on 2022-10-13 00:18

from django.db import migrations
from django.contrib.auth.models import Group, User


def populate_db(apps, schema_editor):
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

    manager_group, createdm = Group.objects.get_or_create(name='Manager')
    customer_group, createdc = Group.objects.get_or_create(name='Customer')
    employee_group, createde = Group.objects.get_or_create(name='Employee')

    manager = User.objects.create_user(username='managerDan', password='imtheboss')
    manager.save()
    manager.groups.add(manager_group)

    employee = User.objects.create_user(username='workerJill', password='ilovetowork')
    employee.save()
    employee.groups.add(employee_group)
    
    customer = User.objects.create_user(username='personJoe', password='goodpassword')
    customer.save()
    customer.groups.add(customer_group)


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]