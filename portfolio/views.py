from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Portfolio
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import EmailForm



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

class PortfolioAboutView(TemplateView):
    model = Portfolio
    template_name = 'about_me.html'
    success_url = reverse_lazy('portfolio_list')
 

class ConfirmView(FormView):
    template_name = 'confirm.html'
    form_class = EmailForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        # Get form data
        name = form.cleaned_data['name']
        sender_email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # Prepare email content
        subject = f"New message from {name}"
        full_message = f"Name: {name}\nEmail: {sender_email}\nMessage:\n{message}"

        try:
            # Send emails
            send_mail(
                subject,
                full_message,
                'techexe.net@gmail.com',
                ['techexe.net@gmail.com'],
                fail_silently=False,
            )

            send_mail(
                "Thank you for your message!",
                "Hi Dear,\n\nThank you for reaching out! We will get back to you soon.\n\nBest regards,\nTechExe",
                'techexe.net@gmail.com',
                [sender_email],
                fail_silently=False,
            )
            print("Emails sent successfully.")

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return self.form_invalid(form)

        return super().form_valid(form)
    
class SuccessView(TemplateView):
    template_name = 'success.html'  # Ensure success.html template exists