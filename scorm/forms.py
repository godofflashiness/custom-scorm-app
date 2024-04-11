from django import forms
from .models import ScormAsset

class ScormUploadForm(forms.ModelForm):
    class Meta:
        model = ScormAsset 
        fields = ['title', 'description', 'scorm_file'] 
        widgets = {'scorm_file': forms.FileInput()}