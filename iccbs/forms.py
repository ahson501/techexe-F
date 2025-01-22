# iccbs/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UpdateUserForm(forms.ModelForm):
    """Form for updating user details."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UpdateProfileForm(forms.ModelForm):
    """Form for updating profile details."""
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']

class RegisterForm(forms.ModelForm):
    """Form for registering new users."""
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        """Validate that the two password entries match."""
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm

    def save(self, commit=True):
        """Save the user instance with a hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user