# core_workflow/urls.py
from django.urls import path
from .views import WorkflowDashboardView, ProcessWorkflowActionView, WorkflowPrintView

urlpatterns = [
    path('dashboard/', WorkflowDashboardView.as_view(), name='workflow_dashboard'),
    
    # 1. Put the print view FIRST so Django matches "/print/" before checking for dynamic action strings
    path('task/<int:instance_id>/print/', WorkflowPrintView.as_view(), name='print_workflow_task'),
    
    # 2. Put the action processor SECOND
    path('task/<int:instance_id>/action/<str:action_type>/', ProcessWorkflowActionView.as_view(), name='process_workflow_action'),
]