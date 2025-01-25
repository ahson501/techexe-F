from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')
