from django.db import models
from django.contrib.auth.models import User

# =========================
# WORKFLOW TEMPLATE
# =========================

class Workflow(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="steps")
    role = models.CharField(max_length=50)  # e.g. supervisor, manager, director
    step_order = models.PositiveIntegerField()

    class Meta:
        ordering = ['step_order']
        unique_together = ('workflow', 'step_order')

    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order} ({self.role})"


# =========================
# MAIN UPLC REQUEST
# =========================

class UPLCRequest(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uplc_requests")
    
    # ADDED THIS: This allows your form to work as you wrote it!
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="supervised_requests")
    
    workflow = models.ForeignKey(Workflow, on_delete=models.SET_NULL, null=True, blank=True)

    # Basic Info
    sample_code = models.CharField(max_length=100)
    intercom = models.CharField(max_length=50, blank=True)

    # Form Fields
    sample_type = models.TextField()
    solubility = models.CharField(max_length=200)
    wavelength = models.FloatField()
    flow_rate = models.FloatField()
    solvent_a = models.CharField(max_length=100, blank=True)
    solvent_b = models.CharField(max_length=100, blank=True)
    column = models.CharField(max_length=200, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True) # Useful for tracking

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.sample_code} ({self.status})"


# =========================
# APPROVAL INSTANCE
# =========================

class Approval(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    request = models.ForeignKey(UPLCRequest, on_delete=models.CASCADE, related_name="approvals")
    step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approvals")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True)
    action_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['step__step_order']
        unique_together = ('request', 'step')

    def __str__(self):
        return f"{self.request.sample_code} - Step {self.step.step_order} - {self.status}"


# =========================
# AUDIT LOG
# =========================

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('updated', 'Updated'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    request = models.ForeignKey(UPLCRequest, on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.request.sample_code} - {self.action}"