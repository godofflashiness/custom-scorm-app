from django import forms
from .models import ScormAsset, ScormAssignment
from clients.models import Client

class ScormUploadForm(forms.ModelForm):
    class Meta:
        model = ScormAsset 
        fields = ['title', 'description', 'category', 'duration','scorm_file'] 
        widgets = {'scorm_file': forms.FileInput()}

class AssignSCORMForm(forms.ModelForm):
    scorms = forms.ModelMultipleChoiceField(queryset=ScormAsset.objects.all(), widget=forms.CheckboxSelectMultiple)
    client = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = ScormAssignment
        fields = ['number_of_seats']