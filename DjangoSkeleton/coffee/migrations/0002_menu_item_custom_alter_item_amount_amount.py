# Generated by Django 4.1.2 on 2022-11-05 21:18

from django.db import migrations, models





class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu_item',
            name='custom',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item_amount',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]
