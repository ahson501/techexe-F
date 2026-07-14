# it_services/views.py
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime

from .models import ITComplaint, EmailAccountCreation, ZoomLinkRegistration
from .forms import ITComplaintForm, EmailAccountCreationForm, ZoomLinkRegistrationForm
from core_workflow.models import WorkflowConfig, WorkflowInstance

class BaseWorkflowCreateView(LoginRequiredMixin, CreateView):
    """ Automatically handles compliance metadata injection and spins up workflow tracking """
    
    # Define compliance metadata mapping for each form model
    COMPLIANCE_METADATA = {
        'ITComplaint': {
            'doc_no': 'ICCBS/QF/QSP-IT/ITCF',
            'revision_no': '08',
            'issue_no': '1',
            'revision_date': datetime.date(2026, 3, 10),
        },
        'EmailAccountCreation': {
            'doc_no': 'ICCBS/QF/QSP-L.T-05',
            'revision_no': '01',
            'issue_no': '1',
            'revision_date': datetime.date(2022, 10, 31),
        },
        'ZoomLinkRegistration': {
            'doc_no': 'ICCBS/DIGITAL/ZOOM',
            'revision_no': '01',
            'issue_no': '1',
            'revision_date': datetime.date(2026, 1, 1),
        }
    }

    def form_valid(self, form):
        # 1. Map current user as author
        form.instance.submitted_by = self.request.user
        
        # 2. Automatically inject missing compliance fields to satisfy database non-null rules
        model_name = self.model.__name__
        meta = self.COMPLIANCE_METADATA.get(model_name, {})
        
        for field, value in meta.items():
            if hasattr(form.instance, field):
                setattr(form.instance, field, value)
                
        # 3. Save instance records safely to PostgreSQL / SQLite
        response = super().form_valid(form)
        
        # 4. Trigger workflow engine tracking instance mapping
        content_type = ContentType.objects.get_for_model(self.object)
        config = WorkflowConfig.objects.filter(content_type=content_type, is_active=True).first()
        
        if config:
            first_step = config.steps.order_by('step_number').first()
            WorkflowInstance.objects.create(
                workflow=config,
                content_type=content_type,
                object_id=self.object.id,
                status='PENDING',
                current_step=first_step,
                submitted_by=self.request.user
            )
            messages.success(self.request, "Form request successfully initialized in the workflow engine!")
        else:
            messages.warning(self.request, "Form saved locally, but no active Workflow configuration matches in the Admin Panel.")
            
        return response


class RaiseComplaintView(BaseWorkflowCreateView):
    model = ITComplaint
    form_class = ITComplaintForm
    template_name = "it_services/raise_complaint.html"
    success_url = reverse_lazy('workflow_dashboard')


class ApplyEmailView(BaseWorkflowCreateView):
    model = EmailAccountCreation
    form_class = EmailAccountCreationForm
    template_name = "it_services/apply_email.html"
    success_url = reverse_lazy('workflow_dashboard')


class RegisterZoomView(BaseWorkflowCreateView):
    model = ZoomLinkRegistration
    form_class = ZoomLinkRegistrationForm
    template_name = "it_services/register_zoom.html"
    success_url = reverse_lazy('workflow_dashboard')