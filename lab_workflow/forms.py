from django import forms
from .models import UPLCRequest, NMRRequest
from django.contrib.auth.models import User

# --- 1. UPLC FORM ---
class UPLCRequestForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, 
        label="Applicant Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    
    precautions_ack = forms.BooleanField(
        label="I have read and understood the precautions", 
        required=True
    )

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
        fields = [
            'supervisor', 'intercom', 'sample_code', 'sample_type', 
            'solubility', 'wavelength', 'flow_rate', 'solvent_a', 
            'solvent_b', 'column',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supervisor'].queryset = User.objects.all()
        for field in self.fields:
            if field != 'solubility' and field != 'precautions_ack':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


# --- 2. NMR FORM (Separated and Fixed Indentation) ---
class NMRRequestForm(forms.ModelForm):
    class Meta:
        model = NMRRequest
        # Note: exclude must be inside Meta
        exclude = ['user', 'date_submitted', 'status']
        
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'thesis_title': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'lab_no': forms.TextInput(attrs={'class': 'form-control'}),
            'extension_no': forms.TextInput(attrs={'class': 'form-control'}),
            'sample_code': forms.TextInput(attrs={'class': 'form-control'}),
            'solvent': forms.TextInput(attrs={'class': 'form-control'}),
            'solubility': forms.TextInput(attrs={'class': 'form-control'}),
            'molecular_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'concentration': forms.TextInput(attrs={'class': 'form-control'}),
            'status_h_nmr': forms.TextInput(attrs={'class': 'form-control'}),
            'status_c_nmr': forms.TextInput(attrs={'class': 'form-control'}),
            'data_format': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom labels for NMR specifics
        if 'status_h_nmr' in self.fields:
            self.fields['status_h_nmr'].label = "Status of 1H NMR"
        if 'status_c_nmr' in self.fields:
            self.fields['status_c_nmr'].label = "Status of 13C NMR"