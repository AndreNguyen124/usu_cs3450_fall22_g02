from django import forms
from .models import Inventory_Item, Menu_Item

from .models import Drink_Item
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NameForm(forms.Form):
    name = forms.CharField(label='commenter-name', max_length=100)


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory_Item
        fields = ['quantity']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink_Item
        fields = ['name', 'Ingredients', 'price']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu_Item
        fields = ['name', 'Ingredients']
