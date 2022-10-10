from django import forms
from .models import Inventory_Item

class NameForm(forms.Form):
    name = forms.CharField(label='commenter-name', max_length=100)

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory_Item
        fields = ['quantity']

