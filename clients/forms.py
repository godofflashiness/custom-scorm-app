from django import forms
from .models import Client 

class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name','contact_email', 'contact_phone', 'company']

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'contact_email', 'contact_phone', 'company']