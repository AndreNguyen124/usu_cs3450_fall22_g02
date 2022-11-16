from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Inventory_Item, Price_Markup, Profile, Item_Amount  # Drink_Item,
from .models import Menu_Item


class NameForm(forms.Form):
    name = forms.CharField(label='commenter-name', max_length=100)


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory_Item
        fields = ['quantity']

class PriceMarkupForm(forms.ModelForm):
    class Meta:
        model = Price_Markup
        fields = ['markup']



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class DrinkForm(forms.ModelForm):
    class Meta:
        model = Menu_Item
        fields = ['name', 'Ingredients']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu_Item
        fields = ['name', 'Ingredients']


class AccountBalanceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['account_balance']
        widgets = {
                'account_balance': forms.NumberInput(attrs={'min': 0}),
                }


class LogHoursForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['hours_worked']
        widgets = {
                'hours_worked': forms.NumberInput(attrs={'min': 0}),
                }

