# it_services/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class RaiseComplaintView(LoginRequiredMixin, TemplateView):
    template_name = "it_services/raise_complaint.html"

class ApplyEmailView(LoginRequiredMixin, TemplateView):
    template_name = "it_services/apply_email.html"

class RegisterZoomView(LoginRequiredMixin, TemplateView):
    template_name = "it_services/register_zoom.html"