from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'bio', 'profile_picture', 'designation', 'country', 'city', 'highest_qualification', 
            'specialization', 'institution', 'skills', 'tools', 'linkedin', 'github', 'google_scholar', 'link1', 'link2', 'link3'
        )
        widgets = {
            'link1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Computational Experiments-01'}),
            'link2': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Computational Experiments-01'}),
            'link3': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Computational Experiments-01'}),
        }
