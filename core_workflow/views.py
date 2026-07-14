# core_workflow/views.py
from django.views.generic import ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import WorkflowInstance

class WorkflowDashboardView(LoginRequiredMixin, ListView):
    model = WorkflowInstance
    template_name = "core_workflow/dashboard.html"
    context_object_name = "workflow_tasks"

    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.all()
        
        # ACTIVE INBOX: What needs action right now
        return WorkflowInstance.objects.filter(
            Q(current_actor=user) | 
            Q(current_step__assigned_group__in=user_groups) | 
            Q(submitted_by=user),
            status='PENDING'
        ).select_related('workflow', 'current_step', 'submitted_by').order_by('-submitted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['action_required_count'] = self.get_queryset().count()
        context['my_submissions_count'] = WorkflowInstance.objects.filter(submitted_by=user).count()
        
        # ─── RESOLVER HISTORY LOGIC ───
        # If the user is in the IT group, show ALL resolved records system-wide.
        # Otherwise, restrict history to only their own items.
        if user.groups.filter(name='it_complains').exists() or user.is_superuser:
            context['history_tasks'] = WorkflowInstance.objects.filter(
                status__in=['COMPLETED', 'REJECTED']
            ).select_related('workflow', 'submitted_by').order_by('-completed_at')
        else:
            context['history_tasks'] = WorkflowInstance.objects.filter(
                Q(submitted_by=user) | Q(current_actor=user),
                status__in=['COMPLETED', 'REJECTED']
            ).select_related('workflow', 'submitted_by').order_by('-completed_at')[:15]
        
        return context


class ProcessWorkflowActionView(LoginRequiredMixin, View):
    def post(self, request, instance_id, action_type):
        instance = get_object_or_404(WorkflowInstance, id=instance_id, status='PENDING')
        
        if action_type == 'approve':
            current_step_number = instance.current_step.step_number
            next_step = instance.workflow.steps.filter(
                step_number__gt=current_step_number
            ).order_by('step_number').first()
            
            if next_step:
                instance.current_step = next_step
                messages.success(request, f"Task #WF-{instance.id} approved and routed forward.")
            else:
                instance.status = 'COMPLETED'
                instance.completed_at = timezone.now()
                messages.success(request, f"Task #WF-{instance.id} has been fully completed!")
                
        elif action_type == 'reject':
            instance.status = 'REJECTED'
            instance.completed_at = timezone.now()
            messages.error(request, f"Task #WF-{instance.id} has been rejected.")
            
        instance.save()
        return redirect('workflow_dashboard')


class WorkflowPrintView(LoginRequiredMixin, DetailView):
    """ Generates a clean, formal, print-optimized document layout """
    model = WorkflowInstance
    template_name = "core_workflow/print_task.html"
    context_object_name = "instance"
    pk_url_kwarg = "instance_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the linked dynamic object (Complaint, Email, or Zoom model instance)
        context['document'] = self.object.form_object
        context['doc_type'] = self.object.content_type.model
        return context