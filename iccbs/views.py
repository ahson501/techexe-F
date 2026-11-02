from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import update_session_auth_hash



# Base Page View
def iccbs_base(request):
    """Render the base template (home page)."""
    return render(request, 'iccbs/base.html')


# Dashboard/Home View
@login_required
def iccbshome(request):
    """Render the home page for logged-in users."""
    return render(request, 'iccbs/iccbshome.html')
# iccbs/views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def force_password_change(request):
    """Force user to set a new password on initial login."""
    if not request.user.profile.must_change_password:
        return redirect('iccbs:iccbs_login')

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Prevent user from being logged out after password change
            update_session_auth_hash(request, form.user)
            
            # Clear mandatory change flag
            request.user.profile.must_change_password = False
            request.user.profile.save()

            messages.success(request, 'Your password has been changed successfully. You may now continue.')
            return redirect('iccbs:iccbshome')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'iccbs/force_password_change.html', {'form': form})
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



class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    """Allows logged-in users to change their password."""
    template_name = 'iccbs/change_password.html'
    success_message = "Your password was successfully updated!"
    success_url = reverse_lazy('iccbs:password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Keeps the user logged in after password change
        # update_session_auth_hash(self.request, self.user)
        return response

class ChangePasswordDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    """Renders success confirmation after password change."""
    template_name = 'iccbs/change_password_done.html'

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
    """Handle user login with role-based redirect."""

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🚨 Check if first login requires password change
            if getattr(user, 'profile', None) and user.profile.must_change_password:
                messages.info(request, 'You are logging in for the first time. Please update your password.')
                return redirect('iccbs:force_password_change')

            messages.success(request, f'Welcome, {user.username}!')

            # IT SERVICES & ENGINE ACTORS REDIRECT
            if user.groups.filter(name__in=['it_complains', 'hod']).exists():
                return redirect('workflow_dashboard')  # Redirects to /workflow/dashboard/

            # LAB WORKFLOW REDIRECT
            if user.groups.filter(name__in=['uplc_student', 'uplc_supervisor', 'nmr_student', 'nmr_supervisor', 'mediate_supervisor', 'final_approvar']).exists():
                return redirect('lab_workflow:post_login_redirect')  # use URL name, not hardcoded path
            
            
            # 🏛️ 1. HOD / DEPARTMENT HEAD
            if user.groups.filter(name='LMS_HOD').exists():
                return redirect('hod_dashboard')

            # 💳 2. ACCOUNTANT / FINANCE
            if user.groups.filter(name='LMS_Accountant').exists():
                return redirect('accountant_dashboard')  # or voucher verification view

            # 📋 3. ADMISSIONS OFFICER
            if user.groups.filter(name='LMS_admissions_officer').exists():
                return redirect('admissions_dashboard')  # or student verification list

            # 👨‍🏫 4. PERMANENT INSTRUCTOR
            if user.groups.filter(name='LMS_Instructor').exists():
                return redirect('instructor_dashboard')

            # 💼 5. VISITING FACULTY
            if user.groups.filter(name='LMS_VisitingFaculty').exists():
                return redirect('visiting_faculty_dashboard')

            # 🎓 6. STUDENT
            if user.groups.filter(name='LMS_Student').exists():
                return redirect('student_dashboard')

            return redirect('iccbs:profile')

        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    else:
        form = AuthenticationForm()

    return render(request, 'iccbs/login.html', {'form': form})


def logout_view(request):
    """Handle user logout and redirect to login page."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    
    # Redirect directly to your login view name
    return redirect('iccbs:iccbs_login')  


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
    success_url = reverse_lazy('iccbs:password_reset_done')

def get_email_context_data(self):
        context = super().get_email_context_data()
        # Dynamically grabs host (e.g., techexe.net or 172.16.2.35)
        context['domain'] = self.request.get_host()
        return context

def public_profile(request, username):
    """Render a public profile page."""
    user = get_object_or_404(User, username=username)
    profile = user.profile  # Assuming you have a `Profile` model related to `User`
    return render(request, 'iccbs/public_profile.html', {'user': user, 'profile': profile})

def contact_me(request):
    return render(request, 'iccbs/contact_me.html')





# iccbs/views.py

import logging

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from .forms import RoleUserCreationForm

logger = logging.getLogger(__name__)


class RegisterView(View):
    template_name = 'iccbs/register.html'

    def get(self, request):
        form = RoleUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RoleUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # 1. Keep account inactive until admin approval
            user.is_active = False
            user.save()

            # 2. Assign selected role
            selected_role = form.cleaned_data.get('role')
            group, _ = Group.objects.get_or_create(name=selected_role)
            user.groups.add(group)

            role_display = (
                "Student" if selected_role == 'LMS_Student'
                else "Instructor"
            )

            # 3. Prepare email notification
            subject = (
                f"TechExe LMS - {role_display} Registration Received"
            )

            email_message = f"""Hello {user.username},

Thank you for registering on TechExe LMS as a {role_display}.

Your registration request has been received successfully.

Your account is currently pending administrative approval. 
You will be able to log in once an administrator or admissions 
officer reviews and activates your account.

Registered Email: {user.email}
Account Type: {role_display}

We appreciate your patience.

Best regards,
TechExe Academic Management
"""

            # 4. Send email and display appropriate notification
            try:
                sent = send_mail(
                    subject=subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                if sent:
                    messages.success(
                        request,
                        "Your registration request has been received "
                        "successfully! Please check your email for "
                        "confirmation and further instructions. "
                        "Your account is awaiting administrative approval."
                    )
                else:
                    messages.warning(
                        request,
                        "Your registration request has been received, "
                        "but the confirmation email could not be sent. "
                        "Please contact the administration for assistance."
                    )

            except Exception:
                logger.exception(
                    "Registration confirmation email failed for %s",
                    user.email
                )

                messages.warning(
                    request,
                    "Your registration request has been received, "
                    "but we could not send the confirmation email. "
                    "Please contact the administration for assistance."
                )

            # 5. Redirect back to registration page
            return redirect(request.path)

        return render(request, self.template_name, {'form': form})