# Generated by Django 4.1.2 on 2022-10-25 18:17

from django.db import migrations, models
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


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.RunPython(populate_db),
    ]
