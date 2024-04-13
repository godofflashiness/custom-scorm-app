from django import forms
from .models import ScormAsset, ScormAssignment
from clients.models import Client


class ScormUploadForm(forms.ModelForm):
    class Meta:
        model = ScormAsset
        fields = ["title", "description", "category", "duration", "scorm_file"]
        widgets = {"scorm_file": forms.FileInput()}


class AssignSCORMForm(forms.ModelForm):
    scorms = forms.ModelMultipleChoiceField(
        queryset=ScormAsset.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(), widget=forms.HiddenInput
    )
    validity_start_date = forms.DateTimeField(widget=forms.DateInput, required=False)
    validity_end_date = forms.DateTimeField(widget=forms.DateInput, required=False)

    class Meta:
        model = ScormAssignment
        fields = ["number_of_seats", "validity_start_date", "validity_end_date"]

    def save(self, client, commit=True):
        selected_scorms = self.cleaned_data["scorms"]
        number_of_seats = self.cleaned_data["number_of_seats"]
        validity_start_date = self.cleaned_data["validity_start_date"]
        validity_end_date = self.cleaned_data["validity_end_date"]

        assignments = []
        for scorm in selected_scorms:
            assignment = ScormAssignment(
                scorm_asset=scorm,
                client=client,
                number_of_seats=number_of_seats,
                validity_start_date=validity_start_date,
                validity_end_date=validity_end_date,
            )
            if commit:
                assignment.save()
            assignments.append(assignment)

        return assignments
