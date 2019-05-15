from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    context = forms.Textarea()
    hashtags = forms.CharField(max_length=200)
    is_published = forms.BooleanField()






    
    
        