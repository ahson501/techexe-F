# core_workflow/services.py
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import WorkflowConfig, WorkflowInstance, WorkflowStep, ApprovalTask, WorkflowLog, WorkflowStatus, TaskStatus

class WorkflowEngineService:
    
    @staticmethod
    def initiate_workflow(form_instance, user):
        """
        Triggers workflow assignment right after a form is saved.
        """
        content_type = ContentType.objects.get_for_model(form_instance)
        config = WorkflowConfig.objects.get(content_type=content_type, is_active=True)
        first_step = config.steps.filter(step_number=1).first()
        
        instance = WorkflowInstance.objects.create(
            content_type=content_type,
            object_id=form_instance.id,
            workflow=config,
            current_step=first_step,
            submitted_by=user,
            status=WorkflowStatus.SUBMITTED
        )
        
        # Route to the first actor
        WorkflowEngineService.route_to_step(instance, first_step)
        return instance

    @staticmethod
    def route_to_step(instance, step):
        """
        Determines the destination assignment targets using your routing rules.
        """
        if not step:
            # No steps left means everything is fully approved!
            instance.status = WorkflowStatus.COMPLETED
            instance.current_step = None
            instance.current_actor = None
            instance.current_group = None
            instance.completed_at = timezone.now()
            instance.save()
            return

        instance.current_step = step
        
        # Resolve dynamic actors using routing logic
        from .routing import resolve_approver  # Avoid circular imports
        approver_user, approver_group = resolve_approver(instance, step)
        
        instance.current_actor = approver_user
        instance.current_group = approver_group
        instance.status = WorkflowStatus.IN_PROGRESS
        instance.save()

        # Create the execution task
        ApprovalTask.objects.create(
            workflow_instance=instance,
            step=step,
            assigned_to=approver_user,
            assigned_group=approver_group,
            status=TaskStatus.PENDING
        )