from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import UpdateUserForm, UpdateProfileForm, RegisterForm
from .models import CustomUsericcbs
from django.contrib.messages.views import SuccessMessageMixin

# View for rendering the base.html template (home page)
def iccbs_base(request):
    """View for rendering the base.html template."""
    return render(request, 'iccbs/base.html')

# View for rendering the iccbshome.html page
def iccbshome(request):
    """View for the iccbshome page."""
    return render(request, 'iccbs/iccbshome.html')

# Class-based view for registration
class RegisterView(View):
    """View to handle user registration."""
    form_class = RegisterForm
    template_name = 'iccbs/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='iccbs:profile')  # Redirect logged-in users to their profile page
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect(to='iccbs:iccbshome')  # Redirect to home page after successful registration
        return render(request, self.template_name, {'form': form})

# Password reset view
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """View to handle password reset."""
    template_name = 'iccbs/password_reset.html'
    email_template_name = 'iccbs/password_reset_email.html'
    subject_template_name = 'iccbs/password_reset_subject.txt'
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. Please check your inbox and spam folder."
    )
    success_url = reverse_lazy('iccbs:iccbshome')

# Custom login view
def login_view(request):
    """Custom login view."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:  # Ensure the user is active
                login(request, user)
                return redirect('iccbs:iccbshome')  # Redirect to home after login
            else:
                messages.error(request, "This account is inactive.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'iccbs/login.html', {'form': form})

# View for user profile
@login_required
def profile(request):
    """View to handle user profile updates."""
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('iccbs:iccbs_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'iccbs/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# Password change view
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """View to handle password change."""
    template_name = 'iccbs/change_password.html'
    success_message = "Your password has been changed successfully!"
    success_url = reverse_lazy('iccbs:iccbs_profile')

# Class-based view for a specific template
class iccbsView(LoginRequiredMixin, TemplateView):
    """Class-based view to render iccbs_template.html."""
    template_name = 'iccbs/iccbs_template.html'