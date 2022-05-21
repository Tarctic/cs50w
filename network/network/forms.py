from django import forms

from .models import *

class PostForm(forms.Form):
    
    content = forms.CharField(label="Content", widget=forms.Textarea())
    content.widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Write your thoughts here...',
            })

    img = forms.URLField(label="Enter Image URL",required=False, widget=forms.URLInput())
    img.widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Image URL',
            })

# Ways to use css with forms:
# 1) Use crispy (find how to get it installed in django, solve env/path issues)
# 2) Use PostForm(forms.Form) without Meta
# 3) Use Meta but separate the form elements - https://stackoverflow.com/questions/50014339/how-to-custom-modelform-with-css-django 
# 4) Use good ol' input fields in the html file (no need of forms.py)
# 5) Use urls (only online images)
# 6) No need of images in your website (you can use any option from 2-4 in that case)