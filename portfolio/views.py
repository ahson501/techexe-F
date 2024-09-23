from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Portfolio, ContactInfo
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import EmailForm  # Ensure EmailForm is defined in forms.py

# Portfolio Views

class PortfolioListView(ListView):
    model = Portfolio
    template_name = 'portfolio_list.html'
    context_object_name = 'object_list'

class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio_detail.html'
    context_object_name = 'portfolio'

class PortfolioCreateView(CreateView):
    model = Portfolio
    template_name = 'portfolio_form.html'
    fields = ['title', 'image', 'description', 'technology', 'date_pub']
    success_url = reverse_lazy('portfolio_list')

class PortfolioUpdateView(UpdateView):
    model = Portfolio
    template_name = 'portfolio_form.html'
    fields = ['title', 'image', 'description', 'technology', 'date_pub']
    success_url = reverse_lazy('portfolio_list')

class PortfolioDeleteView(DeleteView):
    model = Portfolio
    template_name = 'portfolio_confirm_delete.html'
    success_url = reverse_lazy('portfolio_list')

# About and Contact Views

class PortfolioAboutView(TemplateView):
    template_name = 'about_me.html'

class ContactMeView(TemplateView):
    template_name = 'contact_me.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_info = ContactInfo.objects.first()  # Ensure ContactInfo model exists
        context['info'] = contact_info
        return context

# Function-based view for portfolio list with additional context

def portfolio_list(request):
    info = {
        'about': "I am a software developer with experience in Django and Docker...",
        'phone': "123-456-7890",
        'email': "your-email@example.com",
        'github': "https://github.com/yourprofile",
        'linkedin': "https://linkedin.com/in/yourprofile",
        'instagram': "https://instagram.com/yourprofile",
        'facebook': "https://facebook.com/yourprofile",
        'twitter': "https://twitter.com/yourprofile"
    }
    # Return the actual instance of the PortfolioListView, not the class itself
    return PortfolioListView.as_view()(request)

# Confirm View for handling contact form and email submission

class ConfirmView(FormView):
    template_name = 'confirm.html'
    form_class = EmailForm
    success_url = reverse_lazy('success')  # Redirect to the success page after sending

    def form_valid(self, form):
        # Extract form data
        name = form.cleaned_data['name']
        sender_email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # Create the email subject and message for the recipient
        subject = f"New message from {name}"
        full_message = f"Name: {name}\nEmail: {sender_email}\nMessage:\n{message}"

        try:
            # Send the email to the recipient (your email)
            send_mail(
                subject,
                full_message,
                'techexe.net@gmail.com',  # Replace with your sender email
                ['techexe.net@gmail.com'],  # Replace with the actual recipient email
                fail_silently=False,
            )

            # Send an auto-reply to the sender
            send_mail(
                "Thank you for your message!",  # Subject for auto-reply
                "Hi Dear,\n\nThank you for reaching out! We will get back to you soon.\n\nBest regards,\nTechExe",  # Auto-reply message
                'your_email@example.com',  # From email (must be valid)
                [sender_email],  # Send to the person who filled out the form
                fail_silently=False,
            )

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return self.form_invalid(form)

        return super().form_valid(form)
