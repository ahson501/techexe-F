# core_workflow/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class WorkflowDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core_workflow/dashboard.html"