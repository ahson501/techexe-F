# core_workflow/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # We will build your central unified "My Approvals Dashboard" here soon!
    path('dashboard/', views.WorkflowDashboardView.as_view(), name='workflow_dashboard'),
]