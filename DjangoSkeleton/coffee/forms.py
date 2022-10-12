from django import forms
from .models import Inventory_Item
from django.contrib.auth.models import User

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

