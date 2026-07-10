# core_workflow/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import WorkflowConfig
from .services import WorkflowEngineService

# List models that should skip automated submission (e.g., if they handle saving drafts first)
MANUAL_WORKFLOW_MODELS = []

@receiver(post_save)
def auto_trigger_workflow_engine(sender, instance, created, **kwargs):
    """
    Listens globally across all project applications. If a saved model matches
    an active WorkflowConfig, it registers an approval tracking trail automatically.
    """
    if not created or sender.__name__ in MANUAL_WORKFLOW_MODELS:
        return

    try:
        content_type = ContentType.objects.get_for_model(sender)
        # Check if an active workflow configuration profile exists for this model
        if WorkflowConfig.objects.filter(content_type=content_type, is_active=True).exists():
            # Fallback logic assumes user tracking metadata is mapped to the object
            user = getattr(instance, 'submitted_by', None) or getattr(instance, 'user', None)
            if user:
                WorkflowEngineService.initiate_workflow(instance, user)
    except Exception:
        # Prevent signature process initialization failures from stopping database transactions
        pass