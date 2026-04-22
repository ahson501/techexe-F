
# lab_workflow/forms.py

from django import forms
from .models import UPLCRequest
from django.contrib.auth.models import User

class UPLCRequestForm(forms.ModelForm):
    # Extra fields not in the Database Model but needed for the Form
    name = forms.CharField(
        max_length=100, 
        label="Applicant Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    
    precautions_ack = forms.BooleanField(
        label="I have read and understood the precautions", 
        required=True
    )

    # Multi-choice for solubility
    solubility = forms.MultipleChoiceField(
        choices=[
            ('water', 'Water'), 
            ('acetonitrile', 'Acetonitrile'), 
            ('methanol', 'Methanol'), 
            ('chloroform', 'Chloroform')
        ],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = UPLCRequest
        # EVERY field mentioned in your HTML must be in this list
        fields = [
            'supervisor',
            'intercom',
            'sample_code',
            'sample_type',
            'solubility',
            'wavelength',
            'flow_rate',
            'solvent_a',
            'solvent_b',
            'column',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filters supervisor list to show all users (or change to is_staff=True)
        self.fields['supervisor'].queryset = User.objects.all()
        # Add Bootstrap or styling classes here if needed
        for field in self.fields:
            if field != 'solubility' and field != 'precautions_ack':
                self.fields[field].widget.attrs.update({'class': 'form-control'})