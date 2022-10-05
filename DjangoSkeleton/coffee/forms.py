from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='commenter-name', max_length=100)