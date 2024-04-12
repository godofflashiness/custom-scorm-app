from django import forms
from .models import ScormAsset, ScormAssignment

class ScormUploadForm(forms.ModelForm):
    class Meta:
        model = ScormAsset 
        fields = ['title', 'description', 'category', 'duration','scorm_file'] 
        widgets = {'scorm_file': forms.FileInput()}

class AssignSCORMForm(forms.ModelForm):
    scorm_asset = forms.ModelMultipleChoiceField(queryset=ScormAssignment.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = ScormAssignment
        fields = ['scorm_asset', 'number_of_seats']