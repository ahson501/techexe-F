# it_services/forms.py
from django import forms
from .models import ITComplaint, EmailAccountCreation, ZoomLinkRegistration

# ==========================================================
# APPLICANT INITIATION FORMS
# ==========================================================

class ITComplaintForm(forms.ModelForm):
    """ Matches Doc No: ICCBS/QF/QSP-IT/ITCF """
    class Meta:
        model = ITComplaint
        fields = [
            'unit', 'user_type', 'complainer_name', 'supervisor_name', 
            'lab_dept', 'intercom_no', 'problem_description'
        ]
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'user_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'complainer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'supervisor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supervisor/HOD Name'}),
            'lab_dept': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Lab 302 / Accounts'}),
            'intercom_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ext. Number'}),
            'problem_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the technical issue...'}),
        }


class EmailAccountCreationForm(forms.ModelForm):
    """ Matches Doc No: ICCBS/QF/QSP-L.T-05 """
    class Meta:
        model = EmailAccountCreation
        fields = [
            'unit', 'first_name', 'middle_name', 'last_name', 
            'lab_no', 'intercom_no', 'contact_no', 'attendance_id', 
            'requested_email', 'alternate_email'
        ]
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'lab_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lab / Office Location'}),
            'intercom_no': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'attendance_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Biometric Attendance ID'}),
            'requested_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username@iccs.edu'}),
            'alternate_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ZoomLinkRegistrationForm(forms.ModelForm):
    """ Structural entry interface for dynamic ICCBS Zoom webinar links scheduling """
    class Meta:
        model = ZoomLinkRegistration
        fields = ['unit', 'meeting_title', 'scheduled_datetime', 'duration_minutes', 'agenda']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'meeting_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seminar / Thesis Defense / Meeting Title'}),
            'scheduled_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'step': '15'}),
            'agenda': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ==========================================================
# WORKFLOW APPROVAL & PROCESSING FORMS
# ==========================================================

class ITComplaintResolutionForm(forms.ModelForm):
    """ Used exclusively by assigned IT Engineering Staff during execution stages """
    class Meta:
        model = ITComplaint
        fields = ['nature_of_problem', 'it_staff_remarks', 'is_resolved']
        widgets = {
            'nature_of_problem': forms.Select(attrs={'class': 'form-select'}),
            'it_staff_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'IT Engineers notes...'}),
            'is_resolved': forms.NullBooleanSelect(attrs={'class': 'form-select'}),
        }


class GeneralWorkflowActionForm(forms.Form):
    """ 
    Generic signature interface loaded across all application nodes 
    (Supervisors, HODs, Directors) to issue verification logs.
    """
    ACTION_CHOICES = [
        ('APPROVE', 'Verify & Sign Off'),
        ('REJECT', 'Reject completely'),
        ('RETURN', 'Send back for changes'),
    ]
    action = forms.ChoiceField(
        choices=ACTION_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Add notes, budget clearance keys, or modification requests...'
        }), 
        required=False
    )