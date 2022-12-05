
from django import forms


class ContactForm(forms.Form):
    zoekterm = forms.CharField(required=True)