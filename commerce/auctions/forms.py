from django.forms import ModelForm
from django import forms

from .models import User, Listing

class ListForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Title"}))
    desc = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Description'}))
    price = forms.FloatField(label="Starting Price", widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': '$ 0.00'}), min_value = 0.00)
    img = forms.URLField(label="Insert Image URL (Resolution of 16:9 is recommended)",required=False, widget=forms.URLInput(attrs={'class':'form-control','placeholder':'Insert URL'}))
