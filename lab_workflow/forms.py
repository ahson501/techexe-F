from django import forms
from .models import UPLCRequest, NMRRequest
from django.contrib.auth.models import User

# --- 1. UPLC FORM ---
class UPLCRequestForm(forms.ModelForm):
    # Define the exact equipment dropdown choices from the paper master document
    COLUMN_CHOICES = [
        ('', '--- Select a Column ---'),
        ('eclipse_phenyl', '1- Eclipse XDB-Phenyl (4.6 × 75 mm, 3.5 μm)'),
        ('zorbax_cn', '2- Zorbax XDB-CN (4.6 × 75 mm, 3.5 μm)'),
        ('zorbax_c18', '3- Zorbax Eclipse XDB-C18 (3 × 50 mm, 1.8 μm)'),
        ('zorbax_sb_c18', '4- Zorbax SB-C18 (3 × 50 mm, 1.8 μm)'),
        ('poroshell_c18', '5- Poroshell 120 EC-C18 (3 × 50 mm, 2.7 μm)'),
        ('eclipse_c8', '6- ECLIPSE XDB-C8 (3 × 30 mm, 1.8 μm)'),
    ]

    # Force column field to render as a select choice dropdown
    column = forms.ChoiceField(
        choices=COLUMN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UPLCRequest
        # Ensure all your target input elements are listed here:
        fields = [
            'name', 'supervisor', 'appointment_date', 'thesis_document', 
            'intercom', 'sample_code', 'sample_type', 'solubility', 
            'wavelength', 'flow_rate', 'solvent_a', 'solvent_b', 
            'column', 'precautions_ack'
        ]
        
        # Inject standard input controls so users can click and type freely
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'thesis_document': forms.FileInput(attrs={'class': 'form-control'}),
            'intercom': forms.TextInput(attrs={'placeholder': 'e.g. 345', 'class': 'form-control'}),
            'sample_code': forms.TextInput(attrs={'placeholder': 'Sample Code', 'class': 'form-control'}),
            'sample_type': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Plant, animal, synthetic...', 'class': 'form-control'}),
            'wavelength': forms.TextInput(attrs={'placeholder': 'nm', 'class': 'form-control'}),
            'flow_rate': forms.TextInput(attrs={'placeholder': 'Flow rate value', 'class': 'form-control'}),
            'solvent_a': forms.TextInput(attrs={'placeholder': 'Solvent System A', 'class': 'form-control'}),
            'solvent_b': forms.TextInput(attrs={'placeholder': 'Solvent System B', 'class': 'form-control'}),
        }


# --- 2. NMR FORM ---
class NMRRequestForm(forms.ModelForm):
    class Meta:
        model = NMRRequest
        exclude = ['user', 'date_submitted', 'status']
        
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            
            # RESTORED: thesis_title is back to a text box for typing
            'thesis_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title of thesis'}),
            
            # ADDED/UPDATED: If your model field is named thesis_document or similar, map it here:
            'thesis_document': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf, .jpg, .jpeg, .png'}),
            
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
        if 'status_h_nmr' in self.fields:
            self.fields['status_h_nmr'].label = "Status of 1H NMR"
        if 'status_c_nmr' in self.fields:
            self.fields['status_c_nmr'].label = "Status of 13C NMR"

# --- LAST. AIAgent FORM ---

from django import forms

class AIAgentDataForm(forms.Form):
    # Form field matching your thesis/research document pattern
    research_document = forms.FileField(
        label="Upload Research Document / Spectrum / Data File",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.docx,.txt,.md,.csv,.xlsx,.tsv,.fasta,.fastq,.vcf,.gff,.bed,.pdb,.mol,.mol2,.sdf,.smi,.png,.jpg,.jpeg,.tiff',
            'id': 'ai-agent-file-input'
        })
    )
    prompt_message = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ask something about this file...'
        })
    )