from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UpdateUserForm, UpdateProfileForm


# Base Page View
def iccbs_base(request):
    """Render the base template (home page)."""
    return render(request, 'iccbs/base.html')


# Dashboard/Home View
@login_required
def iccbshome(request):
    """Render the home page for logged-in users."""
    return render(request, 'iccbs/iccbshome.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('iccbs:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'iccbs/profile.html', context)

# Registration View
class RegisterView(View):
    """Handle user registration using the default User model."""
    form_class = UserCreationForm
    template_name = 'iccbs/register.html'

    def get(self, request, *args, **kwargs):
        """Display the registration form."""
        if request.user.is_authenticated:
            return redirect('iccbs:iccbshome')  # Redirect if already logged in
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle user registration form submission."""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('iccbs:iccbs_login')  # Redirect after successful registration
        return render(request, self.template_name, {'form': form})


# Login View
def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('iccbs:profile')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'iccbs/login.html', {'form': form})


# Logout View
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('iccbs:iccbs_base')


# Password Reset View
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """Handle password reset."""
    template_name = 'iccbs/password_reset.html'
    email_template_name = 'iccbs/password_reset_email.html'
    subject_template_name = 'iccbs/password_reset_subject.txt'
    success_message = (
        "We've emailed you instructions for resetting your password. "
        "If an account exists with the email entered, check your inbox (and spam folder)."
    )
    success_url = reverse_lazy('iccbs:iccbs_base')